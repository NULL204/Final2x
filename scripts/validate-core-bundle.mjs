import fs from 'node:fs'
import path from 'node:path'
import process from 'node:process'
import { fileURLToPath } from 'node:url'

export function validateCoreBundle(directory) {
  if (!fs.existsSync(directory)) {
    throw new Error(`Core bundle was not found at ${directory}`)
  }

  const pending = [directory]
  let symlinkCount = 0

  while (pending.length > 0) {
    const current = pending.pop()

    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const entryPath = path.join(current, entry.name)

      if (entry.isSymbolicLink()) {
        const link = fs.readlinkSync(entryPath)

        if (path.isAbsolute(link)) {
          throw new Error(`Core bundle contains an absolute symlink: ${entryPath} -> ${link}`)
        }
        if (!fs.existsSync(entryPath)) {
          throw new Error(`Core bundle contains a broken symlink: ${entryPath} -> ${link}`)
        }

        symlinkCount += 1
      }
      else if (entry.isDirectory()) {
        pending.push(entryPath)
      }
    }
  }

  console.log(`Validated ${symlinkCount} portable symlinks in ${directory}`)
}

const invokedPath = process.argv[1] ? path.resolve(process.argv[1]) : undefined

if (invokedPath === fileURLToPath(import.meta.url)) {
  const directory = process.argv[2]

  if (!directory) {
    throw new Error('Usage: node scripts/validate-core-bundle.mjs <bundle-directory>')
  }

  validateCoreBundle(path.resolve(directory))
}
