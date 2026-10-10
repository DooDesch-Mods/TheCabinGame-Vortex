'use strict';

const path = require('path');
const { fs, util } = require('vortex-api');
const config = require('./config.json');
const GAME_ID = config.gameId;
const STEAM_ID = '4406280';
const PROJECT = 'the_cabin_game';
const PAKS = `${PROJECT}/Content/Paks`;
const WIN64 = `${PROJECT}/Binaries/Win64`;
const MODS = `${WIN64}/ue4ss/Mods`;
const CONTAINERS = new Set(['.pak', '.utoc', '.ucas']);
const LOADER_FILES = new Set(['dwmapi.dll', 'xinput1_3.dll']);
const DOC = /^(readme.*|license.*|changelog.*|uninstall.*|credits.*)$/i;

function fail(message) {
  throw new Error(`the cabin game: ${message}`);
}

function archivePath(source) {
  const normalized = source.replace(/\\/g, '/');
  if (normalized.startsWith('/') || normalized.includes(':')
      || normalized.split('/').some(part => part === '..' || part === '.')) {
    fail(`unsafe archive path: ${source}`);
  }
  // Windows ignores trailing periods/spaces and treats device names specially.
  if (normalized.split('/').filter(Boolean).some(part =>
    /[<>"|?*\x00-\x1f]/.test(part) || /[. ]$/.test(part)
    || /^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(part))) {
    fail(`invalid Windows archive path: ${source}`);
  }
  return normalized;
}

function route(source) {
  const lower = source.toLowerCase();
  const parts = source.split('/');
  const projectIndex = parts.findIndex(part => part.toLowerCase() === PROJECT);
  let relative = projectIndex >= 0 ? parts.slice(projectIndex + 1).join('/') : source;
  let relLower = relative.toLowerCase();
  const ext = path.posix.extname(source).toLowerCase();

  if (projectIndex >= 0 && relLower.startsWith('content/paks/')) {
    const payload = relative.slice('Content/Paks/'.length);
    // Existing author layouts, including LogicMods, retain their destination.
    if (!CONTAINERS.has(ext)) fail(`unsupported PAK payload: ${source}`);
    return `${PAKS}/${payload}`;
  }
  if (projectIndex >= 0 && relLower.startsWith('binaries/win64/')) {
    relative = relative.slice('Binaries/Win64/'.length);
    relLower = relative.toLowerCase();
  }
  const ueIndex = relative.split('/').findIndex(part => part.toLowerCase() === 'ue4ss');
  if (ueIndex >= 0) {
    const payload = relative.split('/').slice(ueIndex + 1).join('/');
    if (payload) return `${WIN64}/ue4ss/${payload}`;
  }
  const modsIndex = relative.split('/').findIndex(part => part.toLowerCase() === 'mods');
  if (modsIndex >= 0) {
    const payload = relative.split('/').slice(modsIndex + 1).join('/');
    if (payload) return `${MODS}/${payload}`;
  }
  const basename = path.posix.basename(source);
  if (LOADER_FILES.has(basename.toLowerCase())) return `${WIN64}/${basename}`;
  if (projectIndex >= 0) fail(`unsupported game-root file: ${source}`);
  if (CONTAINERS.has(ext)) return `${PAKS}/~mods/${basename}`;
  if (DOC.test(basename) || lower.startsWith('__macosx/') || basename === '.DS_Store') return undefined;
  fail(`unrecognized mod layout: ${source}. Use game-root paths, Mods/<name>/ or loose PAK containers.`);
}

function installContent(files) {
  // Routing is deliberately pure; Vortex owns deployment and purge.
  return Promise.resolve().then(() => {
    const instructions = [];
    const destinations = new Map();
    for (const source of files) {
      const normalized = archivePath(source);
      if (!normalized || normalized.endsWith('/')) continue;
      const destination = route(normalized);
      if (destination === undefined) continue;
      const key = destination.toLowerCase();
      if (destinations.has(key)) fail(`duplicate destination ${destination}: ${destinations.get(key)} and ${source}`);
      if (/\/paks\/(?:~mods\/)?(?:global|the_cabin_game-windows)\.(pak|utoc|ucas)$/i.test(destination)) {
        fail(`archive attempts to replace a base-game container: ${source}`);
      }
      destinations.set(key, source);
      instructions.push({ type: 'copy', source, destination: path.join(...destination.split('/')) });
    }
    if (instructions.length === 0) fail('archive contains no supported mod files');

    for (const key of destinations.keys()) {
      if (key.endsWith('.utoc') || key.endsWith('.ucas')) {
        const stem = key.slice(0, -5);
        for (const suffix of ['.utoc', '.ucas']) {
          if (!destinations.has(stem + suffix)) fail(`incomplete IoStore pair: ${key}, missing ${stem + suffix}`);
        }
      }
    }
    const hasRuntime = destinations.has(`${WIN64}/ue4ss/ue4ss.dll`.toLowerCase());
    if (!hasRuntime) {
      // Do not overwrite the user's global enable list. Independent mods carry their marker.
      for (const key of destinations.keys()) {
        if (key === `${MODS}/mods.txt`.toLowerCase() || key === `${MODS}/mods.json`.toLowerCase()) {
          fail('standalone mods must not replace mods.txt/mods.json; include <mod>/enabled.txt instead');
        }
        const entry = key.match(/\/ue4ss\/mods\/([^/]+)\/(scripts\/main\.lua|dlls\/main\.dll)$/);
        if (entry && !destinations.has(`${MODS}/${entry[1]}/enabled.txt`.toLowerCase())) {
          fail(`UE4SS mod ${entry[1]} is missing enabled.txt; packaging must enable the mod without editing shared mods.txt`);
        }
      }
    }
    return { instructions };
  });
}

function testSupportedContent(files, gameId) {
  // Claim this game's archives so unsupported files fail visibly instead of falling
  // through to an installer that copies arbitrary files into the game root.
  return Promise.resolve({ supported: gameId === GAME_ID, requiredFiles: [] });
}

function findGame() {
  return util.GameStoreHelper.findByAppId([STEAM_ID], 'steam').then(game => game.gamePath);
}

function prepareForModding(discovery) {
  return fs.ensureDirWritableAsync(discovery.path)
    .then(() => fs.ensureDirWritableAsync(path.join(discovery.path, PROJECT, 'Content', 'Paks', '~mods')))
    .then(() => fs.ensureDirWritableAsync(path.join(discovery.path, PROJECT, 'Binaries', 'Win64', 'ue4ss', 'Mods')));
}

function main(context) {
  const details = { steamAppId: Number(STEAM_ID) };
  if (config.nexusPageId !== null) details.nexusPageId = config.nexusPageId;
  context.registerGame({
    id: GAME_ID,
    name: 'the cabin game',
    mergeMods: true,
    queryPath: findGame,
    queryModPath: () => '.',
    logo: 'gameart.png',
    executable: () => `${PROJECT}.exe`,
    requiredFiles: [`${PROJECT}.exe`, path.join(PROJECT, 'Binaries', 'Win64', `${PROJECT}-Win64-Shipping.exe`)],
    setup: prepareForModding,
    environment: { SteamAppId: STEAM_ID },
    details,
  });
  context.registerInstaller(`${GAME_ID}-content`, 25, testSupportedContent, installContent);
  return true;
}

module.exports = { default: main };
