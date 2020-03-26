import { ILayoutRestorer } from '@jupyterlab/application';
import { ICommandPalette, MainAreaWidget } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
// import { PageConfig, URLExt } from '@jupyterlab/coreutils';
// @ts-ignore
// const bURI = URLExt.join(PageConfig.getBaseUrl(), 'sparkuitaburl');
const bURI1 = '/sparkuitabdns';
const bURI2 = '/sparkuitaburl';
/**
 * Initialization data for the JupyterSparkExt extension.
 */
const extension = {
    id: 'jupyterlab_apod',
    requires: [ICommandPalette, ILayoutRestorer],
    autoStart: true,
    activate: activate
};
function activate(app, palette) {
    console.log('JupyterLab extension jupyterlab_apod is activated!');
    // Create a blank content widget inside of a MainAreaWidget
    const content = new Widget();
    content.addClass('my-apodWidget'); // new line
    const widget = new MainAreaWidget({ content });
    widget.id = 'apod-jupyterlab';
    widget.title.label = 'Astronomy Picture';
    widget.title.closable = true;
    // Add an image element to the content
    let img = document.createElement('img');
    content.node.appendChild(img);
    let summary = document.createElement('h3');
    content.node.appendChild(summary);
    let DNShead = document.createElement('h3');
    content.node.appendChild(DNShead);
    DNShead.innerText = "DNS of Master Node :";
    let dnstext = document.createElement('input');
    content.node.appendChild(dnstext);
    let ref_button = document.createElement('button');
    content.node.appendChild(ref_button);
    let clustersummary = document.createElement('iframe');
    content.node.appendChild(clustersummary);
    let porthead = document.createElement('h3');
    content.node.appendChild(porthead);
    porthead.innerText = "Spark UI Port :";
    let porttext = document.createElement('input');
    content.node.appendChild(porttext);
    let sparkui_button = document.createElement('button');
    content.node.appendChild(sparkui_button);
    let iframe = document.createElement('iframe');
    content.node.appendChild(iframe);
    dnstext.setAttribute("placeholder", "default: 0.0.0.0");
    dnstext.setAttribute("value", "0.0.0.0");
    dnstext.setAttribute("id", "dnstext");
    dnstext.setAttribute("style", "color:Black");
    ref_button.innerText = "Cluster Summary (Refresh)";
    ref_button.onclick = function () {
        let dns_text = document.getElementById('dnstext').value;
        clustersummary.src = bURI1 + dns_text;
        clustersummary.style.height = "30%";
    };
    clustersummary.style.height = "40%";
    clustersummary.style.width = "100%";
    clustersummary.src = bURI1 + "0.0.0.0";
    clustersummary.style.border = "none";
    porttext.setAttribute("id", "porttext");
    porttext.setAttribute("placeholder", "default: 4040");
    porttext.setAttribute("value", "4040");
    porttext.setAttribute("style", "color:Gray");
    sparkui_button.innerText = "Spark UI";
    sparkui_button.onclick = function () {
        let dns_text = document.getElementById('dnstext').value;
        let port_text = document.getElementById('porttext').value;
        let url = dns_text + ":" + port_text;
        iframe.src = bURI2 + url;
        clustersummary.style.height = "30%";
    };
    iframe.style.height = "100%";
    iframe.style.width = "100%";
    iframe.src = "/files/export.html";
    summary.innerText = "GSOC 2020";
    summary.style.float = "right";
    img.src = 'https://openastronomy.org/img/logo/logoOA_svg.png';
    img.width = 162;
    img.height = 75;
    img.id = "logo";
    img.style.float = "right";
    // Add an application command
    const command = 'apod:open';
    app.commands.addCommand(command, {
        label: 'Jupyter Spark Extension',
        execute: () => {
            if (!widget.isAttached) {
                // Attach the widget to the main work area if it's not there
                app.shell.add(widget, 'main');
            }
            // Activate the widget
            app.shell.activateById(widget.id);
        }
    });
    // Add the command to the palette.
    palette.addItem({ command, category: 'Open Astronomy' });
}
export default extension;
