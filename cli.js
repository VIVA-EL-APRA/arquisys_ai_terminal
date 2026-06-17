#!/usr/bin/env node

const { spawn, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const packageDir = path.resolve(__dirname);
const venvDir = path.join(packageDir, '.venv');

function findPython() {
    // Prefer python3 on Linux/Mac, python on Windows
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

function ensureVenv(pythonCmd) {
    // .venv already exists -> use it
    const venvPython = process.platform === 'win32'
        ? path.join(venvDir, 'Scripts', 'python.exe')
        : path.join(venvDir, 'bin', 'python3');

    if (fs.existsSync(venvPython)) return venvPython;

    // .venv exists but incomplete (no python binary) -> recreate
    if (fs.existsSync(venvDir)) {
        fs.rmSync(venvDir, { recursive: true, force: true });
    }

    console.log('Configurando entorno virtual de Python...');

    // Create venv
    const create = spawnSync(pythonCmd, ['-m', 'venv', venvDir], { stdio: 'inherit' });
    if (create.status !== 0) {
        console.error('Error: No se pudo crear el entorno virtual.');
        return null;
    }

    // Install requirements
    const reqPath = path.join(packageDir, 'requirements.txt');
    if (fs.existsSync(reqPath)) {
        console.log('Instalando dependencias de Python...');
        const install = spawnSync(venvPython, ['-m', 'pip', 'install', '-r', reqPath], { stdio: 'inherit' });
        if (install.status !== 0) {
            console.error('Error: No se pudieron instalar las dependencias.');
            return null;
        }
        console.log('Dependencias instaladas correctamente.');
    }

    return venvPython;
}

const pythonCmd = findPython();
if (!pythonCmd) {
    console.error('\x1b[31mError: Python no está instalado o no se encuentra en el PATH.\x1b[0m');
    console.error('Instálalo desde https://www.python.org/downloads/');
    process.exit(1);
}

const pythonExec = ensureVenv(pythonCmd);
if (!pythonExec) {
    console.error('\x1b[31mError: No se pudo configurar el entorno de Python.\x1b[0m');
    console.error('Instala las dependencias manualmente: pip install -r ' + path.join(packageDir, 'requirements.txt'));
    process.exit(1);
}

const mainPy = path.join(packageDir, 'main.py');
const child = spawn(pythonExec, [mainPy], {
    stdio: 'inherit',
    env: { ...process.env, PYTHONPATH: packageDir }
});

child.on('exit', (code) => {
    process.exit(code || 0);
});
