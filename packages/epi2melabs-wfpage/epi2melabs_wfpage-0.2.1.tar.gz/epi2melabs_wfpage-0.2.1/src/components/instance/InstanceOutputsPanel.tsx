import React, { useEffect, useState } from 'react';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowUpRightFromSquare } from '@fortawesome/free-solid-svg-icons';
import { GenericObject } from '../../types';
import StyledLoadingSpinner from '../common/LoadingSpinner';
import { finished } from './StatusIndicator';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { Instance } from './types';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IInstanceOutputsPanel {
  className?: string;
  instanceData: Instance;
  instanceStatus: string;
  app: JupyterFrontEnd;
  docTrack: IDocumentManager;
}

const InstanceOutputsPanel = ({
  className,
  instanceData,
  instanceStatus,
  app,
  docTrack
}: IInstanceOutputsPanel): JSX.Element => {
  const [instanceOutputs, setInstanceOutputs] = useState<GenericObject[]>([]);

  // ------------------------------------
  // Handle instance initialisation
  // ------------------------------------
  const getRelativeInstanceDir = async (instanceData: Instance) => {
    const { curr_dir, base_dir } = await requestAPI<any>('cwd');
    const rel_base_dir = base_dir.replace(curr_dir, '').replace(/^\//, '');
    const basename = instanceData.path
      .replace(/\\/g, '/')
      .split('/')
      .reverse()[0];
    return `${rel_base_dir}/instances/${basename}`;
  };

  const getInstanceOutputs = async (instanceData: Instance | null) => {
    if (instanceData) {
      const relative = await getRelativeInstanceDir(instanceData);
      const path = `${relative}/output`;
      try {
        const files = await (
          await docTrack.services.contents.get(path)
        ).content.filter((Item: any) => Item.type !== 'directory');
        setInstanceOutputs(files);
      } catch (error) {
        console.log('Instance outputs not available yet');
      }
    }
  };

  // ------------------------------------
  // Monitor instance status
  // ------------------------------------
  useEffect(() => {
    getInstanceOutputs(instanceData);
    if (finished.includes(instanceStatus)) {
      return;
    } else {
      const filesMonitor = setInterval(() => {
        getInstanceOutputs(instanceData);
      }, 10000);
      return () => {
        getInstanceOutputs(instanceData);
        clearInterval(filesMonitor);
      };
    }
  }, [instanceStatus]);

  // ------------------------------------
  // Handle opening files
  // ------------------------------------
  const handleOpenOutput = (path: string) => {
    const report: any = docTrack.open(path);
    if (report) {
      report.trusted = true;
    }
  };

  const handleOpenFolder = async (instanceData: Instance) => {
    const path = await getRelativeInstanceDir(instanceData);
    app.commands.execute('filebrowser:go-to-path', { path });
  };

  // ------------------------------------
  // Handle find report
  // ------------------------------------
  const getReport = (instanceData: Instance): null | GenericObject => {
    let report = null;
    if (instanceOutputs.length) {
      instanceOutputs.forEach(Item => {
        if (Item.name === `${instanceData.workflow}-report.html`) {
          report = Item;
        }
      });
    }
    return report;
  };

  // ------------------------------------
  // Handle no outputs message
  // ------------------------------------
  const getNoOutputsMessage = () => {
    if (finished.includes(instanceStatus)) {
      return <h4>Workflow has terminated but no outputs are available.</h4>;
    }
    return (
      <div>
        <StyledLoadingSpinner />
      </div>
    );
  };

  const report = getReport(instanceData);
  return (
    <div className={`instance-outputs ${className}`}>
      <div className="instance-outputs-header">
        <h3>Output files</h3>
        <div>
          <button
            onClick={() => (instanceData ? handleOpenFolder(instanceData) : '')}
          >
            Open folder
          </button>
          {report ? (
            <button onClick={() => handleOpenOutput(report.path)}>
              Open report
            </button>
          ) : (
            ''
          )}
        </div>
      </div>
      <div className="instance-outputs-items">
        {instanceOutputs.length ? (
          <ul>
            {instanceOutputs.map(Item => (
              <li>
                <button onClick={() => handleOpenOutput(Item.path)}>
                  <h4>{Item.name}</h4>
                  <FontAwesomeIcon icon={faArrowUpRightFromSquare} />
                </button>
              </li>
            ))}
          </ul>
        ) : (
          getNoOutputsMessage()
        )}
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledInstanceOutputsPanel = styled(InstanceOutputsPanel)`
  && {
    border-radius: 4px;
    padding: 25px;
    margin: 0 0 50px 0;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
  }

  .instance-outputs-header {
    padding-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .instance-outputs-header button {
    margin-left: 15px;
    padding: 10px 24px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    font-size: 13px;
    line-height: 1em;
    transition: 0.2s ease-in-out all;
    background-color: #eee;
    cursor: pointer;
  }

  .instance-outputs-items li button {
    width: 100%;
    padding: 15px 0;
    display: flex;
    border-radius: 0;
    justify-content: space-between;
    align-items: center;
    outline: none;
    background-color: transparent;
    border: none;
    border-top: 1px solid #f2f2f2;
    cursor: pointer;
  }

  .instance-outputs-items li button svg {
    color: #eee;
  }

  .instance-outputs-items li:hover button svg {
    color: #ccc;
  }
`;

export default StyledInstanceOutputsPanel;
