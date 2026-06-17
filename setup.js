#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');

const packageDir = path.resolve(__dirname);
const venvDir = path.join(packageDir, '.venv');
const homeDir = require('os').homedir();

function findPython() {
    const candidates = process.platform === 'win32'
        ? ['python', 'py', 'python3']
        : ['python3', 'python'];
    for (const cmd of candidates) {
        try {
            const r = spawnSync(cmd, ['--version'], { stdio: 'pipe' });
            if (r.status === 0) return cmd;
        } catch (_) { }
    }
    return null;
}

console.log('\x1b[36m\x1b[1m╔══════════════════════════════════════════════════════════════╗\x1b[0m');
console.log('\x1b[36m\x1b[1m║              ArquiSysAI - Configuración Inicial              ║\x1b[0m');
console.log('\x1b[36m\x1b[1m╚══════════════════════════════════════════════════════════════╝\x1b[0m\n');

// ── Create .arquisys-ai.env if missing ──
const envPath = path.join(homeDir, '.arquisys-ai.env');
if (!fs.existsSync(envPath)) {
    console.log('\x1b[33mCreando archivo de configuración...\x1b[0m');
    const envContent = `# ArquiSysAI Configuration
# Get your API key from https://opencode.ai

OPENCODE_API_KEY=sk-placeholder-requires-setup
`;
    fs.writeFileSync(envPath, envContent);
    console.log(`\x1b[32m✓ Archivo de configuración creado en: ${envPath}\x1b[0m`);
}

// ── Python venv setup ──
const pythonCmd = findPython();
if (!pythonCmd) {
    console.log('\x1b[33mAdvertencia: Python no encontrado. Instala las dependencias manualmente.\x1b[0m');
    process.exit(0);
}

const venvPython = process.platform === 'win32'
    ? path.join(venvDir, 'Scripts', 'python.exe')
    : path.join(venvDir, 'bin', 'python3');

if (fs.existsSync(venvPython)) {
    console.log('\x1b[32m✓ Entorno virtual ya configurado\x1b[0m');
} else {
    console.log('\x1b[33mCreando entorno virtual de Python...\x1b[0m');
    try {
        execSync(`"${pythonCmd}" -m venv "${venvDir}"`, { stdio: 'inherit' });
        console.log('\x1b[32m✓ Entorno virtual creado\x1b[0m');
    } catch (e) {
        console.log('\x1b[33mAdvertencia: No se pudo crear el entorno virtual.\x1b[0m');
    }
}

// ── Install Python dependencies ──
const requirementsPath = path.join(packageDir, 'requirements.txt');
if (fs.existsSync(requirementsPath) && fs.existsSync(venvPython)) {
    console.log('\x1b[33mInstalando dependencias de Python...\x1b[0m');
    try {
        execSync(`"${venvPython}" -m pip install -r "${requirementsPath}"`, { stdio: 'inherit' });
        console.log('\x1b[32m✓ Dependencias instaladas correctamente\x1b[0m');
    } catch (error) {
        console.log('\x1b[33mAdvertencia: No se pudieron instalar las dependencias automáticamente.\x1b[0m');
        console.log(`Ejecuta manualmente: ${venvPython} -m pip install -r "${requirementsPath}"`);
    }
}

// ── Done ──
console.log('\n\x1b[32m\x1b[1m╔══════════════════════════════════════════════════════════════╗\x1b[0m');
console.log('\x1b[32m\x1b[1m║           ¡Instalación completada exitosamente!               ║\x1b[0m');
console.log('\x1b[32m\x1b[1m╚══════════════════════════════════════════════════════════════╝\x1b[0m\n');
console.log('Para comenzar, ejecuta: \x1b[36marquisys-ai\x1b[0m\n');
