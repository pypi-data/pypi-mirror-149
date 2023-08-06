import { IMainMenu } from '@jupyterlab/mainmenu';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator } from '@jupyterlab/translation';
import { ContextMenuSvg } from '@jupyterlab/ui-components';
import { CommandRegistry } from '@lumino/commands';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

import { Token } from '@lumino/coreutils';

const BASE = 'jupyterlab_mutableai';

export const PLUGIN_ID = `${BASE}:IMutableAI`;

export const IMutableAI = new Token<IMutableAI>(`${BASE}:IMutableAI`);

export interface IMutableAI {
  enable: () => void;
  disable: () => void;
}

export namespace IMutableAI {
  /**
   * MutableAI constructor options
   */
  export interface IOptions {
    /* 
      Jupyter lab core modules translator.
    */
    translator?: ITranslator;

    /* 
      Jupyter lab core modules main menu.
    */
    mainMenu: IMainMenu;
    /* 
      Jupyter lab apps commands registry.
    */
    commands: CommandRegistry;
    /* 
      Jupyter lab apps context menu port.
    */
    contextMenu: ContextMenuSvg;
    /* 
      Jupyter lab factory registry port.
    */
    factory: IFileBrowserFactory;
    /* 
      Jupyter lab Doc registry port.
    */
    docRegistry: DocumentRegistry;

    /**
     * Extension settings getter
     */
    getSettings: () => Promise<ISettingRegistry.ISettings>;
  }
}
