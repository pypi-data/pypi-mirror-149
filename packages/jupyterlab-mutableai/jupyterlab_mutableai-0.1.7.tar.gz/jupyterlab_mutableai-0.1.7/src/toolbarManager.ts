import { NotebookPanel, INotebookModel } from '@jupyterlab/notebook';

import { ITranslator } from '@jupyterlab/translation';

import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { MutableAiRunner } from './widgets/Toolbar';
import { DocumentRegistry } from '@jupyterlab/docregistry';

interface IActionHandlers {
  onLunchToProduction: (
    context: DocumentRegistry.IContext<INotebookModel>
  ) => void;
  onDocToProduction: (
    context: DocumentRegistry.IContext<INotebookModel>
  ) => void;
  onCustomCommand: (context: DocumentRegistry.IContext<INotebookModel>) => void;
  onRefactorToProduction: (
    context: DocumentRegistry.IContext<INotebookModel>
  ) => void;
}

interface IButtonConfig {
  trans?: ITranslator;
  handlers: IActionHandlers;
}

export class ToolbarWidget
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  constructor(config: IButtonConfig) {
    this._trans = config.trans;
    this._handlers = config.handlers;
  }
  /**
   * Create a new extension for the notebook panel widget.
   *
   * @param panel Notebook panel
   * @param context Notebook context
   * @returns Disposable on the added button
   */
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    const button = new MutableAiRunner(
      panel.content,
      this._handlers,
      context,
      this._trans
    );
    panel.toolbar.insertItem(10, 'Mutable AI', button);
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
  private _trans?: ITranslator;
  private _handlers: IActionHandlers;
}

interface IMutableAiToolbarManagerConfig {
  docRegistry: DocumentRegistry;
  trans?: ITranslator;
  handlers: IActionHandlers;
}

export class ToolbarManager {
  constructor(config: IMutableAiToolbarManagerConfig) {
    this._docRegistry = config.docRegistry;
    this._trans = config.trans;
    this._handlers = config.handlers;
  }
  initialize() {
    const toolbarItem = new ToolbarWidget({
      trans: this._trans,
      handlers: this._handlers
    });

    this._toolbar = this._docRegistry.addWidgetExtension(
      'Notebook',
      toolbarItem
    );
  }
  dispose() {
    this._toolbar?.dispose();
  }
  private _toolbar?: IDisposable;
  private _docRegistry: DocumentRegistry;
  private _trans?: ITranslator;
  private _handlers: IActionHandlers;
}
