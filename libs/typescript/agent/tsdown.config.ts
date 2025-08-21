import { defineConfig } from "tsdown";

export default defineConfig({
  entry: ["src/index.ts"],
  format: ["module"],
  platform: "browser",
  dts: true,
  clean: true,
  noExternal: ['peerjs']
});
