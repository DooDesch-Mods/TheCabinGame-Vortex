'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

const root = path.resolve(__dirname, '..');
const extension = path.join(root, 'extension');
let game, installer;
const discoveryCalls = [];
const vortex = {
  fs: { ensureDirWritableAsync: target => fs.promises.mkdir(target, { recursive: true }) },
  util: { GameStoreHelper: { findByAppId: async (...args) => {
    discoveryCalls.push(args);
    return { gamePath: 'F:/Launcher/SteamLibrary/steamapps/common/the cabin game' };
  } } },
};
const sandbox = {
  module: { exports: {} },
  require: name => name === 'vortex-api' ? vortex
    : name === './config.json' ? JSON.parse(fs.readFileSync(path.join(extension, 'config.json'), 'utf8'))
    : require(name),
};
vm.runInNewContext(fs.readFileSync(path.join(extension, 'index.js'), 'utf8'), sandbox, { filename: 'index.js' });
sandbox.module.exports.default({
  registerGame: value => { game = value; },
  registerInstaller: (id, priority, supported, install) => { installer = { id, priority, supported, install }; },
});
const slash = value => value.replace(/\\/g, '/');
const destinations = async files => (await installer.install(files)).instructions.map(i => slash(i.destination));
const PAK = 'the_cabin_game/Content/Paks';
const WIN = 'the_cabin_game/Binaries/Win64';
const MOD = `${WIN}/ue4ss/Mods`;
const script = ['Mods/CabinRejoin/Scripts/main.lua', 'Mods/CabinRejoin/enabled.txt'];

test('registration targets the confirmed game and Steam app, without inventing a Nexus domain', async () => {
  assert.equal(game.name, 'the cabin game');
  assert.equal(game.environment.SteamAppId, '4406280');
  assert.equal(game.details.steamAppId, 4406280);
  assert.equal(game.executable(), 'the_cabin_game.exe');
  assert.equal(game.queryModPath(), '.');
  assert.equal(game.mergeMods, true);
  const config = JSON.parse(fs.readFileSync(path.join(extension, 'config.json'), 'utf8'));
  assert.equal(game.details.nexusPageId, config.nexusPageId === null ? undefined : config.nexusPageId);
  assert.equal(await game.queryPath(), 'F:/Launcher/SteamLibrary/steamapps/common/the cabin game');
  assert.equal(JSON.stringify(discoveryCalls[0]), JSON.stringify([['4406280'], 'steam']));
  assert.equal((await installer.supported([], 'palworld')).supported, false);
  assert.equal((await installer.supported([], config.gameId)).supported, true);
});

test('loose and wrapped PAK/IoStore files install together', async () => {
  assert.equal(JSON.stringify(await destinations(['Release/CabinRejoin_P.pak', 'Release/CabinRejoin_P.utoc', 'Release/CabinRejoin_P.ucas', 'README.md'])),
    JSON.stringify(['.pak', '.utoc', '.ucas'].map(ext => `${PAK}/~mods/CabinRejoin_P${ext}`)));
});

test('canonical PAK and LogicMods paths retain author intent', async () => {
  const input = [`Release/${PAK}/~mods/Fix.pak`, `${PAK}/LogicMods/Widget.pak`];
  assert.equal(JSON.stringify(await destinations(input)), JSON.stringify(input.map(x => x.replace('Release/', ''))));
});

test('Palvolve-style and fully rooted Lua/native mod packages preserve their relative content', async () => {
  assert.equal(JSON.stringify(await destinations(script)), JSON.stringify(script.map(x => `${MOD}/${x.slice(5)}`)));
  const full = [`${MOD}/CabinRejoin/dlls/main.dll`, `${MOD}/CabinRejoin/enabled.txt`, `${MOD}/CabinRejoin/config.json`];
  assert.equal(JSON.stringify(await destinations(full)), JSON.stringify(full));
});

test('mixed slash styles and mixed PAK/UE4SS content are supported', async () => {
  const result = await destinations([...script.map(x => x.replace(/\//g, '\\')), 'Fix.pak']);
  assert.equal(result.length, 3);
  assert.equal(result[0], `${MOD}/CabinRejoin/Scripts/main.lua`);
});

test('an explicit UE4SS runtime archive retains its loader, config and stock enable list', async () => {
  const input = ['dwmapi.dll', 'ue4ss/UE4SS.dll', 'ue4ss/UE4SS-settings.ini', 'ue4ss/Mods/mods.txt'];
  const output = await destinations(input);
  assert.equal(JSON.stringify(output), JSON.stringify(input.map(x => `${WIN}/${x}`)));
});

for (const [name, files, expected] of [
  ['IoStore companion missing', ['Fix.utoc'], /incomplete IoStore/],
  ['ambiguous variants', ['Low/Fix.pak', 'High/Fix.pak'], /duplicate destination/],
  ['case collision', ['Fix.pak', 'fix.PAK'], /duplicate destination/],
  ['traversal', ['../Fix.pak'], /unsafe archive path/],
  ['absolute drive path', ['C:\\Fix.pak'], /unsafe archive path/],
  ['UNC path', ['\\\\server\\Fix.pak'], /unsafe archive path/],
  ['reserved Windows device', ['CON.pak'], /invalid Windows/],
  ['trailing Windows alias', ['Folder. /Fix.pak'], /invalid Windows/],
  ['base container', [`${PAK}/the_cabin_game-Windows.pak`], /base-game container/],
  ['unknown executable', ['Patch.exe'], /unrecognized mod layout/],
  ['game executable replacement', ['the_cabin_game/Binaries/Win64/the_cabin_game-Win64-Shipping.exe'], /unsupported game-root/],
  ['missing activation marker', ['Mods/CabinRejoin/Scripts/main.lua'], /missing enabled.txt/],
  ['shared activation overwrite', ['Mods/mods.txt', ...script], /must not replace/],
  ['documentation only', ['README.md'], /no supported mod files/],
]) {
  test(`rejects ${name} with an observable cause`, async () => assert.rejects(installer.install(files), expected));
}

test('isolated setup, hardlink deployment, disable, re-enable and purge preserve stock files', async () => {
  fs.mkdirSync(path.join(root, 'evidence'), { recursive: true });
  const fixture = fs.mkdtempSync(path.join(root, 'evidence', 'deployment-'));
  const install = path.join(fixture, 'game');
  const staging = path.join(fixture, 'staging');
  fs.mkdirSync(install);
  fs.mkdirSync(staging);
  const original = path.join(install, ...`${PAK}/the_cabin_game-Windows.pak`.split('/'));
  fs.mkdirSync(path.dirname(original), { recursive: true });
  fs.writeFileSync(original, 'unchanged stock fixture');
  await game.setup({ path: install });
  const files = ['CabinRejoin_P.pak', ...script];
  const { instructions } = await installer.install(files);
  for (const instruction of instructions) {
    const staged = path.join(staging, instruction.destination);
    fs.mkdirSync(path.dirname(staged), { recursive: true });
    fs.writeFileSync(staged, instruction.source.endsWith('enabled.txt') ? '' : `fixture:${instruction.source}`);
  }
  const deploy = () => {
    for (const instruction of instructions) {
      const target = path.join(install, instruction.destination);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.linkSync(path.join(staging, instruction.destination), target);
      assert.equal(fs.readFileSync(target, 'utf8'), fs.readFileSync(path.join(staging, instruction.destination), 'utf8'));
    }
  };
  const purge = () => {
    for (const instruction of instructions) fs.unlinkSync(path.join(install, instruction.destination));
  };
  deploy(); purge();
  for (const instruction of instructions) assert.equal(fs.existsSync(path.join(install, instruction.destination)), false);
  deploy(); purge();
  assert.equal(fs.readFileSync(original, 'utf8'), 'unchanged stock fixture');
  fs.writeFileSync(path.join(fixture, 'receipt.json'), JSON.stringify({ status: 'confirmed', method: 'isolated filesystem simulation; not Vortex UI', installed: instructions.length, disable: true, reenable: true, purge: true, originalPreserved: true }, null, 2));
  console.log(`evidence: ${fixture}`);
});
