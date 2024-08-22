const path = require('path');
const { spawn } = require('child_process');

class AgentZero {
  constructor() {
    this.agentPath = path.resolve(__dirname, '../agent-zero');
  }

  async runCommand(command) {
    return new Promise((resolve, reject) => {
      const process = spawn('python', [
        path.join(this.agentPath, 'main.py'),
        command
      ]);

      let output = '';

      process.stdout.on('data', (data) => {
        output += data.toString();
      });

      process.stderr.on('data', (data) => {
        console.error(`Agent Zero Error: ${data}`);
      });

      process.on('close', (code) => {
        if (code === 0) {
          resolve(output);
        } else {
          reject(`Agent Zero exited with code ${code}`);
        }
      });
    });
  }
}

module.exports = AgentZero;