import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const source = path.join(root, 'core', 'dist', 'Final2x-core')
const target = path.join(root, 'resources', 'Final2x-core')

if (!fs.existsSync(source)) {
  throw new Error(`Core bundle was not found at ${source}`)
}

fs.rmSync(target, { force: true, recursive: true })
fs.cpSync(source, target, { recursive: true })
console.log(`Staged Final2x-core in ${target}`)
