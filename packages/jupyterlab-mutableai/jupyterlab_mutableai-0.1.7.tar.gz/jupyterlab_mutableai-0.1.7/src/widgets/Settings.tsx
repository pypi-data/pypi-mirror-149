import { ReactWidget } from '@jupyterlab/apputils';

import { showDialog, Dialog } from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import React, { useState, useEffect } from 'react';

/**
 * React component for a Mutable AI settings.
 *
 * @returns The React component
 */

type Props = {
  setting: ISettingRegistry.ISettings;
  close: () => void;
};

const SettingsComponent = (props: Props): JSX.Element => {
  const { setting, close } = props;
  const [autoCompleteFlag, setAutoCompleteFlag] = useState<boolean>(false);
  const [apiKey, setApiKey] = useState<string>('');
  const [autocompleteDomain, setAutocompleteDomain] = useState<string>('');
  const [transformDomain, setTransformDomain] = useState<string>('');

  const setValues = () => {
    // Read the settings and convert to the correct type
    setAutoCompleteFlag(setting.get('flag').composite as boolean);
    setApiKey(setting.get('apiKey').composite as string);
    setAutocompleteDomain(
      setting.get('autocompleteDomain').composite as string
    );
    setTransformDomain(setting.get('transformDomain').composite as string);
  };

  const restoreToDefault = () => {
    /*
     * This fetches the default settings from
     * user settings then sets then sets it
     * in the form. But as the form is not
     * submitted it is not saved until save
     * button is pressed.
     */
    const flagDefault = setting.default('flag') as boolean;
    const apiKeyDefault = setting.default('apiKey') as string;
    const autocompleteDomainDefault = setting.default(
      'autocompleteDomain'
    ) as string;
    const transformDomainDefault = setting.default('transformDomain') as string;

    setAutoCompleteFlag(flagDefault);
    setApiKey(apiKeyDefault);
    setAutocompleteDomain(autocompleteDomainDefault);
    setTransformDomain(transformDomainDefault);

    setting.set('flag', flagDefault);
    setting.set('apiKey', apiKeyDefault);
    setting.set('autocompleteDomain', autocompleteDomainDefault);
    setting.set('transformDomain', transformDomainDefault);
  };

  /*
   * Whenever the settings object is changed from
   * outside the widget it updates the form accordingly.
   */
  setting.changed.connect(setValues);

  useEffect(() => {
    /*
     * When the widget is attached.
     * It gets the last values from
     * settings object and updates the
     * settings form.
     */
    setValues();
  }, []);

  const handleSubmit = (e: any) => {
    /*
     * This function gets the submitted form
     * It then updates the values from form-data
     * After that the latest data is saved in user-settings.
     * Also after successful saving it shows a
     */

    e.preventDefault();
    const okButton = Dialog.okButton({
      className: 'btn jp-mutableai-modal-btn'
    });

    try {
      setting.set('flag', autoCompleteFlag);
      setting.set('apiKey', apiKey);
      setting.set('autocompleteDomain', autocompleteDomain);
      setting.set('transformDomain', transformDomain);

      // Success dialog.
      showDialog({
        title: 'Mutable AI Settings',
        body: 'The changes saved successfully!',
        buttons: [okButton]
      });
    } catch (e: any) {
      // Error dialog.
      showDialog({
        title: 'Mutable AI Settings',
        body: 'Something went wrong saving settings. Reason: ' + e.toString(),
        buttons: [okButton]
      });
    }
  };

  return (
    <div className="jp-mutableai-container">
      <h1>Mutable AI Settings</h1>
      <div className="jp-mutableai-header">
        <button
          className="btn btn-secondary"
          type="button"
          onClick={restoreToDefault}
        >
          Restore to Defaults
        </button>
      </div>
      <form className="jp-mutableai-form" onSubmit={handleSubmit}>
        <div className="jp-mutableai-group ">
          <label>Autocomplete Flag</label>
          <input
            type="checkbox"
            checked={autoCompleteFlag}
            onChange={e => setAutoCompleteFlag(e.target.checked)}
          />
          <span>This controls whether or not autocomplete is activated.</span>
        </div>
        <div className="jp-mutableai-group ">
          <label>API key</label>
          <input
            className="form-control"
            placeholder=""
            type="text"
            value={apiKey}
            onChange={e => setApiKey(e.target.value)}
          />
          <span>This is the api key to call the endpoints.</span>
        </div>
        <div className="jp-mutableai-group ">
          <label>Autocomplete Domain</label>
          <input
            className="form-control"
            placeholder=""
            type="text"
            value={autocompleteDomain}
            onChange={e => setAutocompleteDomain(e.target.value)}
          />
          <span>Used to construct url to call autocomplete endpoint</span>
        </div>
        <div className="jp-mutableai-group ">
          <label>Transform Domain</label>
          <input
            className="form-control"
            placeholder=""
            type="text"
            value={transformDomain}
            onChange={e => setTransformDomain(e.target.value)}
          />
          <span>Used to construct url to call transform endpoint</span>
        </div>
        <div className="jp-mutableai-footer">
          <button className="btn btn-secondary" type="button" onClick={close}>
            Cancel
          </button>
          <button className="btn btn-success" type="submit">
            Save
          </button>
        </div>
      </form>
    </div>
  );
};

export class SettingsWidget extends ReactWidget {
  /**
   * Constructs a new Settings Widget.
   */
  public setting: ISettingRegistry.ISettings;
  public closeShell: () => void;

  constructor(setting: ISettingRegistry.ISettings, close: () => void) {
    super();

    // This is the top widget class for settings widget.
    this.addClass('jp-mutableai-widget');

    // settings object passed here is used.
    // This is used to get, set, update
    // mutable AI settings.
    this.setting = setting;

    // This is used to close the shell.
    this.closeShell = close;
  }

  render(): JSX.Element {
    // This is the settings component passed to the widget.
    return (
      <SettingsComponent
        setting={this.setting}
        close={() => this.closeShell()}
      />
    );
  }
}
