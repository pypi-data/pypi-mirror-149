import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ILauncher } from '@jupyterlab/launcher';
import { PageConfig } from '@jupyterlab/coreutils';
import { LabIcon } from '@jupyterlab/ui-components';

import IconStr from '../style/Logo.svg';
const MosaicIcon = new LabIcon({ name: 'mosaic:open', svgstr: IconStr });

/**
 * Initialization data for the jupyterlab-mosaic extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
    id: 'jupyterlab-mosaic:plugin',
    autoStart: true,
    requires: [ILauncher],
    activate: (app: JupyterFrontEnd, launcher: ILauncher) => {
        console.log('JupyterLab extension jupyterlab-mosaic is activated!');

        const command = "mosaic:open"
        const url = new URL("mosaic", PageConfig.getBaseUrl());
        app.commands.addCommand(command, {
            label: "Open Mosaic",
            icon: MosaicIcon,
            execute: args => {
                window.open(url.href, 'libman');
            }
        });

        const launcher_item: ILauncher.IItemOptions = {
            command: command,
            category: 'Schematic',
        };
        launcher.add(launcher_item);
    }
};

export default plugin;
