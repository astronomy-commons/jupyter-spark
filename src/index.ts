import {
  JupyterFrontEndPlugin,JupyterFrontEnd
} from "@jupyterlab/application";

import { 
  ICommandPalette, MainAreaWidget 
} from "@jupyterlab/apputils";

import { 
  Widget 
} from "@lumino/widgets";

function activate(
  this: JupyterFrontEndPlugin<void>,
  app: JupyterFrontEnd,
  palette: ICommandPalette
): void {
  console.log("In activate");

  /* Create Widget view for the Spark UI */
  const sparkUiWidget = new Widget();
  sparkUiWidget.title.label = "Spark UI Widget";

  const widget = new MainAreaWidget({ content: sparkUiWidget });
  widget.id = "spark-ui";
  widget.title.label = "Jupyterlab Spark UI";
  widget.title.closable = true;
  
  const heading = document.createElement("h2");
  heading.innerHTML = "Spark Extension - Shwetanshu Rohatgi";
  heading.style.marginLeft = "10px";
  heading.style.marginTop = "10px";
  heading.style.fontFamily = 'Open Sans';
  const sparkContainer = document.createElement("div");
  sparkContainer.style.textAlign = "center";
  sparkContainer.style.height = "200px";

  let fetchDataOfPySparkFromDropdown = (event: Event) => {
    console.log((<HTMLInputElement>event.target).value);
    (document.getElementById("portnumber") as HTMLInputElement).value = (<
      HTMLInputElement
    >event.target).value;
    fetchDataOfPySpark();
  };
  let fetchDataOfPySpark = async () => {
    let portNumber = (document.getElementById("portnumber") as HTMLInputElement)
      .value;

    try {
      document.getElementById(
        "applicationRes"
      ).innerHTML = `<p>Fetching App Data..</p>`;
      document.getElementById(
        "executorRes"
      ).innerHTML = `<p>Fetching App Executors..</p>`;
      document.getElementById(
        "environmentRes"
      ).innerHTML = `<p>Fetching Environmental Variables and Dependencies...</p>`;

      let applicationResponse = await fetch(
        `http://localhost:${portNumber}/api/v1/applications/`
      );
      let applicationResult = await applicationResponse.json();
      console.log("result is ", applicationResult);
      document.getElementById("applicationRes").innerHTML = `
      <p>PySpark App Data</p>
      <p>Number of apps running on ports : ${applicationResult.length}</p>
        <ol>
        <li>Application ID: ${applicationResult[0].id}</li>
        <li>Application Name: ${applicationResult[0].name}</li>
        </ol>
      `;
      let appId = applicationResult[0].id;
      let executorsResponse = await fetch(
        `http://localhost:${portNumber}/api/v1/applications/${appId}/executors`
      );
      let executors = await executorsResponse.json();
      console.log("executors", executors);
      document.getElementById("executorRes").innerHTML = `
      <p>App Executors Data</p>
      <ol>
      <li>Executor Id: ${executors[0].id}</li>
      <li>Host Port: ${executors[0].hostPort}</li>
      <li>Add Time: ${executors[0].addTime}</li>
      <li>Max Memory Use: ${executors[0].maxMemory}</li>
      </ol>
    `;
      let environmentResponse = await fetch(
        `http://localhost:${portNumber}/api/v1/applications/${appId}/environment`
      );
      let environment = await environmentResponse.json();
      console.log("environment", environment);
      document.getElementById("environmentRes").innerHTML = `
      <p>Environmental Data</p>
      <ol>
      <li>Java Version: ${environment.runtime.javaVersion}</li>
      <li>Java Home: ${environment.runtime.javaHome}</li>
      <li>Scala Version: ${environment.runtime.scalaVersion}</li>
      </ol>
    `;
    } catch (err) {
      document.getElementById(
        "applicationRes"
      ).innerHTML = `<p>Error! application data not found.</p>`;
      document.getElementById(
        "executorRes"
      ).innerHTML = `<p>Error! executors data not found</p>`;
      document.getElementById(
        "environmentRes"
      ).innerHTML = `<p>Error! environment data and variables not found.</p>`;
      console.log("There was an error");
    }
  };
  let listOfAllPorts = new Array();
  let fetchListOfAllPorts = async (initialPort: any) => {
    try {
      (document.getElementById("getPorts") as HTMLFormElement).disabled = true;
      document.getElementById(
        "getPorts"
      ).innerHTML = `Getting data of all active ports...`;
      let apiRes = await fetch(
        `http://localhost:${initialPort}/api/v1/applications/`
      );
      if (apiRes) {
        listOfAllPorts.push(initialPort);
      }
      fetchListOfAllPorts(initialPort + 1);
    } catch (err) {
      (document.getElementById("selectPort") as HTMLFormElement).innerHTML = "";
      (document.getElementById("getPorts") as HTMLFormElement).disabled = false;
      document.getElementById("getPorts").innerHTML = `Fetch all active ports`;

      let selectElement = document.getElementById(
        "selectPort"
      ) as HTMLFormElement;
      listOfAllPorts.map(eachPort => {
        selectElement.add(new Option(`Port ${eachPort}`, eachPort));
      });
      
      listOfAllPorts = new Array();
      console.log(listOfAllPorts);
    }
  };
  /* Create input field */
  const submitButton = document.createElement("button");
  submitButton.id = "submitBtn";
  submitButton.style.marginLeft = "10px";
  submitButton.style.marginTop = "10px";
  submitButton.innerHTML = "Get Details";
  submitButton.onclick = () => fetchDataOfPySpark();

  const getPortsButton = document.createElement("button");
  getPortsButton.id = "getPorts";
  getPortsButton.style.marginLeft = "10px";
  getPortsButton.style.marginTop = "10px";
  getPortsButton.innerHTML = "Fetch all active ports";
  getPortsButton.onclick = () => fetchListOfAllPorts(4040);

  const portInput = document.createElement("div");
  portInput.innerHTML = `<div class="wrapper">
      <p>Show Used Port Details</p>
      <input class="input" id="portnumber" placeholder="Enter Port Number" type="text"></div>`;
  portInput.style.marginLeft = "10px";
  portInput.style.marginTop = "10px";

  const select = document.createElement("select");
  select.id = "selectPort";
  select.style.marginLeft = "10px";
  select.style.marginTop = "10px";
  select.onchange = () => fetchDataOfPySparkFromDropdown(event);

  const applicationResponse = document.createElement("div");
  applicationResponse.setAttribute("id", "applicationRes");
  const executorsResponse = document.createElement("div");
  executorsResponse.setAttribute("id", "executorRes");
  const environmentResponse = document.createElement("div");
  environmentResponse.setAttribute("id", "environmentRes");

  sparkUiWidget.node.appendChild(heading);
  sparkUiWidget.node.appendChild(portInput);
  sparkUiWidget.node.appendChild(submitButton);
  sparkUiWidget.node.appendChild(getPortsButton);
  sparkUiWidget.node.appendChild(select);

  sparkUiWidget.node.appendChild(applicationResponse);
  sparkUiWidget.node.appendChild(executorsResponse);
  sparkUiWidget.node.appendChild(environmentResponse);
  sparkUiWidget.node.appendChild(sparkContainer);

  /* Add an application command */
  const command: string = "spark:open";
  app.commands.addCommand(command, {
    label: "Spark UI Widget",
    execute: () => {
      if (!widget.isAttached) {
        // Attach the widget to the main work area if it's not there
        app.shell.add(widget, "main");
      }
      // Refresh the widget
      sparkUiWidget.update();
      // Activate the widget
      app.shell.activateById(widget.id);
    }
  });

  /* Add the command to the palette. */
  palette.addItem({ command, category: "Spark" });
}

/**
 * Refactor code: Initialization data for the spark_ui_tab extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: "spark_ui",
  autoStart: true,
  requires: [ICommandPalette],
  activate: activate
};

export default extension;