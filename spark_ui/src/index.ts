import {
  JupyterFrontEndPlugin, JupyterFrontEnd
} from '@jupyterlab/application';
import {
  ICommandPalette,
  MainAreaWidget,
} from '@jupyterlab/apputils';

import {
  Widget
} from '@lumino/widgets';

import '../style/index.css';

function activate(this: JupyterFrontEndPlugin<void>, app: JupyterFrontEnd, palette: ICommandPalette): void {
  console.log('In activate');

  /* Create main view components */
  const sparkWidget = new Widget();
  sparkWidget.title.label = 'Open Spark UI';
  const widget = new MainAreaWidget({ content: sparkWidget });
  widget.id = 'spark-ui';
  widget.title.label = 'Spark UI';
  widget.title.closable = true;
  const heading = document.createElement('h1');
  heading.innerHTML = 'Access the Spark UI';
  heading.style.marginLeft = '5%';
  const sparkContainer = document.createElement('div');
  sparkContainer.style.textAlign = 'center';
  sparkContainer.style.height = '70vh';

  /* Gets frame according to newly inputted port number */
  function changeIFrame(event: { preventDefault: () => void; }) {
    // Prevents page refresh
    event.preventDefault();
    const portNumber = parseInt((<HTMLInputElement>document.getElementById('portnumber')).value);
    const link = `http://localhost:${portNumber}/jobs/`;
    console.log(`This is the link: ${link}, ${portNumber}`);
    sparkContainer.innerHTML = `<iframe src="${link}" width="95%" height="100%"></iframe>`;
  }

  /* Create input field */
  const form = document.createElement('form');
  form.style.marginLeft = '5%';
  form.style.marginBottom = '2em';

  /* Call function to display new IFrame when form submitted */
  if (form.addEventListener) {
    form.addEventListener('submit', changeIFrame, false);
  } else {
    form.attachEvent('onsubmit', changeIFrame);
  }

  const input = document.createElement('div');
  input.innerHTML = 
    '<div class="wrapper">\
      <span>Get Spark UI (typically at port numbers at and after 4040) \
      <input class="input" id="portnumber" placeholder="4040" type="text">\
      <input class="submit-button" type="submit" value="Go"></span>\
    </div>';
  form.appendChild(input);
  
  /* Add elements to the view */
  sparkWidget.node.appendChild(heading);
  sparkWidget.node.appendChild(form);
  sparkWidget.node.appendChild(sparkContainer);

  /* Add an application command */
  const command: string = 'spark:open';
  app.commands.addCommand(command, {
    label: 'Spark UI',
    execute: () => {
      if (!widget.isAttached) {
        // Attach the widget to the main work area if it's not there
        app.shell.add(widget, 'main');
      }
      // Refresh the picture in the widget
      sparkWidget.update();
      // Activate the widget
      app.shell.activateById(widget.id);
    }
  });
  
  /* Add the command to the palette. */
  palette.addItem({ command, category: 'Spark' });
}

/**
* Initialization data for the spark_ui_tab extension.
*/
const extension: JupyterFrontEndPlugin<void> = {
  id: 'spark_ui',
  autoStart: true,
  requires: [ICommandPalette],
  activate: activate
};

export default extension;   