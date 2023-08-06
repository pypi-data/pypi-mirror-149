import { IMainMenu, MainMenu } from '@jupyterlab/mainmenu';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { ContextMenuSvg, RankedMenu } from '@jupyterlab/ui-components';
import { InputDialog } from '@jupyterlab/apputils';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { INotebookModel } from '@jupyterlab/notebook';
import { PromiseDelegate } from '@lumino/coreutils';
import { IMutableAI } from './tokens';
import { toggleFlag, updateSettings } from './commands';
import { CommandRegistry } from '@lumino/commands';
import { IDisposable } from '@lumino/disposable';
import {
  fastForwardIcon,
  documentIcon,
  customDocIcon,
  refactorIcon
} from './icons';

import {
  context_custom,
  context_documentation,
  context_refactor,
  context_fast_forward
} from './commands';

import { ToolbarManager } from './toolbarManager';
import { requestAPI } from './handler';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

enum mode {
  FULL = 'FULL',
  DOCUMENT = 'DOCUMENT',
  FREE = 'FREE',
  REFACTOR = 'REFACTOR'
}

export class MutableAIManager implements IMutableAI {
  constructor(options: IMutableAI.IOptions) {
    this.mutableAiMainMenu = null;
    this._translator = options.translator ?? nullTranslator;
    this._mainMenu = options.mainMenu;
    this._commands = options.commands;
    this._contextMenu = options.contextMenu;
    this._factory = options.factory;
    this._processFilePointer = null;
    this.onLunchToProduction = this.onLunchToProduction.bind(this);
    this.onDocToProduction = this.onDocToProduction.bind(this);
    this.onCustomCommand = this.onCustomCommand.bind(this);
    this.onRefactorToProduction = this.onRefactorToProduction.bind(this);
    this._toolbarManager = new ToolbarManager({
      docRegistry: options.docRegistry,
      handlers: {
        onLunchToProduction: this.onLunchToProduction,
        onDocToProduction: this.onDocToProduction,
        onCustomCommand: this.onCustomCommand,
        onRefactorToProduction: this.onRefactorToProduction
      },
      trans: options.translator
    });

    options
      .getSettings()
      .then(mutableAI => {
        this._mutableAI = mutableAI;
        this._mutableAI.changed.connect(this._mutableAISettingsChanged, this);
        this._mutableAISettingsChanged();
        this._ready.resolve();
      })
      .catch(reason => {
        console.warn(reason);
        this._ready.reject(reason);
      });
  }

  /*
    Mutable AI manager extension enable port.
  */
  enable() {
    this._mutableAI?.set('enabled', true);
  }

  /*
    Mutable AI manager extension disable port.
  */
  disable() {
    this._mutableAI?.set('enabled', false);
  }

  private handleLunchToProductionCall(name: string) {
    const apiKey = this._mutableAI?.get('apiKey').composite as string;
    const transformDomain = this._mutableAI?.get('transformDomain')
      .composite as string;

    const dataToSend = { name, apiKey, transformDomain, mode: mode.FULL };

    const reply = requestAPI<any>('TRANSFORM_NB', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    });

    reply
      .then(response => console.log('Transformed Successfully!'))
      .catch(e => console.log('Transformation failed!', e));
  }

  private onLunchToProduction(
    context: DocumentRegistry.IContext<INotebookModel>
  ) {
    const name = context.path;
    this.handleLunchToProductionCall(name);
  }

  private handleDocToProductionCall(name: string) {
    const apiKey = this._mutableAI?.get('apiKey').composite as string;
    const transformDomain = this._mutableAI?.get('transformDomain')
      .composite as string;

    const dataToSend = { name, apiKey, transformDomain, mode: mode.DOCUMENT };
    const reply = requestAPI<any>('TRANSFORM_NB', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    });

    reply
      .then(response => console.log('Transformed doc Successfully!'))
      .catch(e => console.log('Transformation failed!', e));
  }

  private onRefactorToProduction(
    context: DocumentRegistry.IContext<INotebookModel>
  ) {
    const name = context.path;
    this.handleRefactorToProductionCall(name);
  }

  private handleRefactorToProductionCall(name: string) {
    const apiKey = this._mutableAI?.get('apiKey').composite as string;
    const transformDomain = this._mutableAI?.get('transformDomain')
      .composite as string;

    const dataToSend = { name, apiKey, transformDomain, mode: mode.REFACTOR };
    const reply = requestAPI<any>('TRANSFORM_NB', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    });

    reply
      .then(response => console.log('Transformed doc Successfully!'))
      .catch(e => console.log('Transformation failed!', e));
  }

  private onDocToProduction(
    context: DocumentRegistry.IContext<INotebookModel>
  ) {
    const name = context.path;
    this.handleDocToProductionCall(name);
  }

  private async handleCustomCommandCall(name: string) {
    // Prompt the user about the statement to be executed
    const input = await InputDialog.getText({
      title: 'Mutable AI Custom Command',
      okLabel: 'Execute',
      placeholder: 'Custom Commands'
    });

    // Execute the statement
    if (input.button.accept) {
      const commands = input.value;

      const apiKey = this._mutableAI?.get('apiKey').composite as string;
      const transformDomain = this._mutableAI?.get('transformDomain')
        .composite as string;

      const dataToSend = {
        name,
        apiKey,
        transformDomain,
        instruction: commands,
        mode: mode.FREE
      };

      const reply = requestAPI<any>('TRANSFORM_NB', {
        body: JSON.stringify(dataToSend),
        method: 'POST'
      });

      reply
        .then(response => console.log('Transformed doc Successfully!'))
        .catch(e => console.log('Transformation failed!', e));
    }
  }

  private onCustomCommand(context: DocumentRegistry.IContext<INotebookModel>) {
    const name = context.path;
    this.handleCustomCommandCall(name);
  }

  private createContextMenu() {
    /*
      Mutable AI update settings in main menu command.
    */
    this._forwardRef = this._commands.addCommand(context_fast_forward, {
      label: `Fast forward to production`,
      icon: fastForwardIcon,
      execute: () => {
        const file = this._factory.tracker.currentWidget
          ?.selectedItems()
          .next();
        if (file?.path) {
          this.handleLunchToProductionCall(file.path);
        }
      }
    });

    this._docRef = this._commands.addCommand(context_documentation, {
      label: 'Document all methods',
      icon: documentIcon,
      execute: () => {
        const file = this._factory.tracker.currentWidget
          ?.selectedItems()
          .next();
        if (file?.path) {
          this.handleDocToProductionCall(file.path);
        }
      }
    });

    this._refactorRef = this._commands.addCommand(context_refactor, {
      label: 'Refactor file',
      icon: refactorIcon,
      execute: () => {
        const file = this._factory.tracker.currentWidget
          ?.selectedItems()
          .next();
        if (file?.path) {
          this.handleRefactorToProductionCall(file.path);
        }
      }
    });

    this._customRef = this._commands.addCommand(context_custom, {
      label: 'Custom command',
      icon: customDocIcon,
      execute: () => {
        const file = this._factory.tracker.currentWidget
          ?.selectedItems()
          .next();
        if (file?.path) {
          this.handleCustomCommandCall(file.path);
        }
      }
    });
  }

  /*
    Mutable AI manager extension initialization.
  */
  private initializePlugin() {
    this.dispose();
    const enabled = this._mutableAI?.get('enabled').composite as boolean;
    if (enabled) {
      this._toolbarManager.initialize();
      this.createContextMenu();
      const trans = this._translator.load('jupyterlab');

      this.mutableAiMainMenu = MainMenu.generateMenu(
        this._commands,
        {
          id: 'mutable-ai-settings',
          label: 'Mutable AI Settings',
          rank: 80
        },
        trans
      );

      this.mutableAiMainMenu.addGroup([
        {
          command: toggleFlag
        },
        {
          command: updateSettings
        }
      ]);

      this._mainMenu.addMenu(this.mutableAiMainMenu, { rank: 80 });

      this._processFilePointer = this._contextMenu.addItem({
        command: 'context_menu:open',
        selector: '.jp-DirListing-item[data-file-type="notebook"]',
        rank: 0
      });
    }
  }

  /*
    Mutable AI manager extension dispose.
  */
  private dispose() {
    this.mutableAiMainMenu?.dispose();
    this._processFilePointer?.dispose();
    this._toolbarManager.dispose();

    this._forwardRef?.dispose();
    this._docRef?.dispose();
    this._customRef?.dispose();
    this._refactorRef?.dispose();
  }

  /**
   * A promise that resolves when the settings have been loaded.
   */
  get ready(): Promise<void> {
    return this._ready.promise;
  }

  /**
   * Mutable AI manager change extension according to settings.
   */
  private _mutableAISettingsChanged(): void {
    const enabled = this._mutableAI?.get('enabled').composite as boolean;
    if (enabled) {
      this.initializePlugin();
    } else {
      this.dispose();
    }
  }

  mutableAiMainMenu: RankedMenu | null;
  private _factory: IFileBrowserFactory;
  private _contextMenu: ContextMenuSvg;
  private _processFilePointer: IDisposable | null;
  private _commands: CommandRegistry;
  private _ready = new PromiseDelegate<void>();
  private _translator: ITranslator;
  private _mainMenu: IMainMenu;
  private _mutableAI: ISettingRegistry.ISettings | null = null;
  private _toolbarManager: ToolbarManager;
  private _forwardRef: IDisposable | undefined;
  private _docRef: IDisposable | undefined;
  private _customRef: IDisposable | undefined;
  private _refactorRef: IDisposable | undefined;
}
