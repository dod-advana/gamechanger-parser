# README

## Quick Start
If the Docker image `gc-parser` is already built, start the container with this command:

\```bash
docker run -it -p 8888:8888 gc-parser 2>&1 | awk '/Or copy and paste one of these URLs:/{exit}1'
\```

To find the running container's ID, use:

\```bash
docker ps
\```

To stop the container, execute:

\```bash
docker stop <CONTAINER_ID>
\```

Replace `<CONTAINER_ID>` with the actual ID of your container.

## Initial Setup

### Requirements
- Visual Studio Code (VS Code)

### Default Values
- `CONTAINER_NAME=gc-parser`
- `IMAGE_NAME=gc-parser`
- `PORT=8888:8888`

Modify `./setupDockerEnv.sh` to adjust default values.

Run `./setupDockerEnv.sh` to download required dependencies and map the container's port to `PORT` value.

After container and image setup, a log will provide access URLs:

![Screenshot of Links Provided When Jupyter Server Starts](screenshotWalkthrough/JupLabLink.png)

Copy and paste the second URL into your browser.

## Additional Steps for VS Code Development

1. Navigate to `config/test.ipynb` in your browser to initialize the kernel. No import errors should occur:

   ![Jupyter Lab with successful test notebook run](screenshotWalkthrough/JupLabTestNotebook.png)

2. In VS Code, connect to your running container:
   - Click the blue icon at the bottom left.
   - Select "Attach to running container".
   - Choose `gc-parser` (default).

If the app's directory isn't visible, open a terminal in VS Code (attached to the container) and execute:

\```bash
cd /home
code .
\```

The IDE should look like this:

![Screenshot of IDE with app dir while connected to container](screenshotWalkthrough/containerIDE.png)

3. In VS Code, reopen `config/test.ipynb`:
   - Choose the kernel at the top right of the notebook.
   - If prompted, install the Jupyter Extension:

     ![Jupyter Extension Help](screenshotWalkthrough/JupExt.png)

   - Select "Existing Kernel" and use the URL that allowed browser access (e.g., `http://0a22027336b5:8888/tree?token=r4and0mNumb3rs`).
   - Enter the autofilled IP address and select `ipykernel`.

You're now set to execute the notebook in your container through VS Code, automatically syncing your Jupyter Labs environment.