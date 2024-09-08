# Mac M1 Diagnostics and UV Usage Guide

## Diagnostic Commands for Mac M1

1. System Information:
   ```
   system_profiler SPHardwareDataType
   ```

2. CPU and Memory Usage:
   ```
   top
   ```

3. Disk Usage:
   ```
   df -h
   ```

4. List of Running Processes:
   ```
   ps aux
   ```

5. Network Statistics:
   ```
   netstat -an
   ```

6. GPU Information:
   ```
   system_profiler SPDisplaysDataType
   ```

7. Rosetta 2 Status (for x86 apps):
   ```
   sysctl -n sysctl.proc_translated
   ```

8. Check for Software Updates:
   ```
   softwareupdate --list
   ```

9. System Log:
   ```
   log show --last 1h
   ```

10. Temperature and Fan Speed:
    ```
    sudo powermetrics --samplers smc -i1 -n1
    ```

## UV Usage Guide

When converting from pip to UV, here are some guidelines:

1. Replace `pip install` with `uv pip install`:
   ```
   uv pip install package_name
   ```

2. For requirements files:
   ```
   uv pip install -r requirements.txt
   ```

3. To create a virtual environment with UV:
   ```
   uv venv
   ```

4. To activate the UV virtual environment:
   ```
   source .venv/bin/activate
   ```

5. To install packages in editable mode:
   ```
   uv pip install -e .
   ```

## Virtual Environments Best Practices

1. Always use virtual environments for Python projects, even if not explicitly mentioned in install instructions.

2. Create a new virtual environment for each project to isolate dependencies.

3. When you see `pip install` without mention of a venv:
   - Create and activate a virtual environment first
   - Then run the install command within the activated environment

4. To create a virtual environment with standard tools:
   ```
   python3 -m venv myenv
   source myenv/bin/activate
   ```

5. Add your virtual environment directory (e.g., `venv`, `.venv`, `env`) to your `.gitignore` file.

6. Consider using `pyproject.toml` for modern Python packaging, which UV supports.

Remember, using UV or traditional virtual environments is about isolating project dependencies and maintaining a clean development environment. Always prioritize this isolation, regardless of the tool you're using.

