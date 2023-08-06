import React from 'react';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { ReactWidget } from '@jupyterlab/apputils';
import { IDocumentManager } from '@jupyterlab/docmanager';
import StyledInstance from './components/instance/Instance';
import StyledWorkflow from './components/workflow/Workflow';
import StyledNotebooksPanel from './components/notebook/NotebooksIndex';
import StyledWorkflowsPanel from './components/workflow/WorkflowsIndex';
import StyledHeader from './components/common/Header';
import StyledFooter from './components/common/Footer';
import styled from 'styled-components';

import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

const LauncherContainer = styled.div``;

export class Launcher extends ReactWidget {
  constructor(
    app: JupyterFrontEnd,
    docTrack: IDocumentManager,
    settings: ISettingRegistry.ISettings
  ) {
    super();
    this.app = app;
    this.docTrack = docTrack;
    this.settings = settings;
    this.addClass('jp-ReactWidget');
    this.addClass('epi2melabs-wfpage-widget');
  }

  render(): JSX.Element {
    return (
      <Router>
        <LauncherContainer>
          <main style={{ position: 'relative' }}>
            <StyledHeader />
            <div>
              <Routes>
                <Route path="/workflows/:name">
                  <Route path=":instance_id" element={<StyledWorkflow />} />
                  <Route path="" element={<StyledWorkflow />} />
                </Route>
                <Route path="/workflows" element={<StyledWorkflowsPanel />} />
                <Route
                  path="/instances/:id"
                  element={
                    <StyledInstance docTrack={this.docTrack} app={this.app} />
                  }
                />
                <Route
                  path="/notebooks"
                  element={
                    <StyledNotebooksPanel
                      docTrack={this.docTrack}
                      templateDir={
                        this.settings.get('template_dir').composite as string
                      }
                      workDir={
                        this.settings.get('working_dir').composite as string
                      }
                    />
                  }
                />
                <Route path="/" element={<StyledWorkflowsPanel />} />
              </Routes>
            </div>
            <StyledFooter />
          </main>
        </LauncherContainer>
      </Router>
    );
  }

  public app: JupyterFrontEnd;
  public docTrack: IDocumentManager;
  public settings: ISettingRegistry.ISettings;
}
