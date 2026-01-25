#!/usr/bin/env bun
/**
 * Bun Build Script Template
 *
 * Usage:
 *   bun run build.js
 *   bun run build.js --watch
 *   bun run build.js --dev
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";

const distDir = "./dist";
const isWatch = process.argv.includes("--watch");
const isDev = process.argv.includes("--dev");

if (!existsSync(distDir)) {
  mkdirSync(distDir, { recursive: true });
}

console.log(`Building ${isDev ? "development" : "production"} bundles...\n`);

const commonOptions = {
  minify: !isDev,
  sourcemap: isDev ? "inline" : "none",
  target: "browser",
  format: "esm",
  define: {
    "process.env.NODE_ENV": isDev ? '"development"' : '"production"',
  },
};

async function build() {
  const startTime = Date.now();

  try {
    const result = await Bun.build({
      ...commonOptions,
      entrypoints: ["./src/index.js"],
      outdir: distDir,
      naming: "bundle.min.js",
      external: [],
    });

    if (!result.success) {
      console.error("Build failed:");
      result.logs.forEach(log => console.error(log));
      process.exit(1);
    }

    // Report sizes
    const files = ["bundle.min.js"];
    console.log("Bundle sizes:");
    for (const file of files) {
      const path = join(distDir, file);
      if (existsSync(path)) {
        const size = (readFileSync(path).length / 1024).toFixed(1);
        console.log(`  ${file.padEnd(25)} ${size} KB`);
      }
    }

    console.log(`\nBuild completed in ${Date.now() - startTime}ms`);
  } catch (error) {
    console.error("Build error:", error);
    process.exit(1);
  }
}

await build();

if (isWatch) {
  console.log("\nWatching for changes...");
  const fs = await import("fs");
  fs.watch("./src", { recursive: true }, async (_, filename) => {
    if (filename?.endsWith(".js") || filename?.endsWith(".ts")) {
      console.log(`\nFile changed: ${filename}`);
      await build();
    }
  });
  process.stdin.resume();
}
