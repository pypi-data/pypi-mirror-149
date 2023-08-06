import React, { useEffect, useState } from 'react';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { IDocumentManager } from '@jupyterlab/docmanager';
import StyledTabbedHeader, { ITabbedHeaderTab } from '../common/TabbedHeader';
import { useParams, useNavigate } from 'react-router-dom';
import StyledStatusIndicator from './StatusIndicator';
import StyledLoadingSpinner from '../common/LoadingSpinner';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { Instance } from './types';
import StyledInstanceLogsPanel from './InstanceLogsPanel';
import StyledInstanceOutputsPanel from './InstanceOutputsPanel';
import StyledInstanceParamsPanel from './InstanceParamsPanel';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IInstanceComponent {
  className?: string;
  docTrack: IDocumentManager;
  app: JupyterFrontEnd;
}

const InstanceComponent = ({
  className,
  docTrack,
  app
}: IInstanceComponent): JSX.Element => {
  const navigate = useNavigate();
  const routerParams = useParams();
  const [selectedTab, setSelectedTab] = useState(0);
  const [instanceStatus, setInstanceStatus] = useState<string>('');
  const [instanceData, setInstanceData] = useState<Instance | null>(null);

  // ------------------------------------
  // Handle instance initialisation
  // ------------------------------------
  const getInstanceData = async () => {
    const data = await requestAPI<any>(`instances/${routerParams.id}`);
    setInstanceData(data);
    setInstanceStatus(data.status);
    return data;
  };

  useEffect(() => {
    const init = async () => {
      await getInstanceData();
    };
    init();
    const statusMonitor = setInterval(() => getInstanceData(), 5000);
    return () => {
      clearInterval(statusMonitor);
    };
  }, []);

  // ------------------------------------
  // Handle instance deletion
  // ------------------------------------
  const handleInstanceDelete = async (d: boolean) => {
    const outcome = await requestAPI<any>(`instances/${routerParams.id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        delete: d
      })
    });
    if (d && outcome.deleted) {
      navigate('/workflows');
    }
  };

  // ------------------------------------
  // Render loading screen
  // ------------------------------------
  if (!instanceData) {
    return (
      <div className={`instance ${className}`}>
        <div className="loading-screen">
          <p>
            Instance data is loading... (If this screen persists, check
            connection to jupyterlab server and/or labslauncher)
          </p>
          <StyledLoadingSpinner />
        </div>
      </div>
    );
  }

  // ------------------------------------
  // Tabbed interface
  // ------------------------------------
  const isRunning = ['LAUNCHED'].includes(instanceStatus);
  const tabs: ITabbedHeaderTab[] = [
    {
      body: 'Workflow outputs',
      onClick: () => setSelectedTab(0),
      element: (
        <div className="tab-contents">
          <StyledInstanceOutputsPanel
            instanceData={instanceData}
            instanceStatus={instanceStatus}
            app={app}
            docTrack={docTrack}
          />
          <StyledInstanceLogsPanel
            title="Workflow logs"
            logfile="nextflow.stdout"
            instanceData={instanceData}
            instanceStatus={instanceStatus}
          />
        </div>
      )
    },
    {
      body: 'Instance details',
      onClick: () => setSelectedTab(1),
      element: (
        <div className="tab-contents">
          <StyledInstanceParamsPanel instanceData={instanceData} />
          <StyledInstanceLogsPanel
            title="Instance logs"
            logfile="invoke.stdout"
            instanceData={instanceData}
            instanceStatus={instanceStatus}
          />
        </div>
      )
    },
    {
      body: isRunning ? 'Stop instance' : 'Delete instance',
      className: 'instance-delete',
      onClick: () => handleInstanceDelete(!isRunning)
    }
  ];

  return (
    <div className={`instance ${className}`}>
      <div className="instance-container">
        <StyledTabbedHeader
          title={instanceData.name}
          body={
            <div className="instance-details">
              <div className="instance-status">
                <StyledStatusIndicator status={instanceStatus || 'UNKNOWN'} />
                <p>{instanceStatus}</p>
              </div>
              <p>{instanceData.workflow}</p>
              <p>Last Updated: {instanceData.updated_at}</p>
            </div>
          }
          active={selectedTab}
          tabs={tabs}
        />

        {tabs[selectedTab].element}
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledInstanceComponent = styled(InstanceComponent)`
  background-color: #f6f6f6;

  .loading-screen {
    display: flex;
    justify-content: center;
    min-height: calc(100vh - 100px);
    align-items: center;
    flex-direction: column;
  }

  .loading-screen p {
    text-align: center;
    max-width: 600px;
    padding-bottom: 15px;
  }

  .instance-container {
    box-sizing: border-box;
    padding: 0 0 50px 0 !important;
  }

  @keyframes fadeInUp {
    from {
      transform: translate3d(0, 40px, 0);
    }

    to {
      transform: translate3d(0, 0, 0);
      opacity: 1;
    }
  }

  .tab-contents {
    box-sizing: border-box;
    width: 100%;
    max-width: calc(1024px + 30px);
    padding: 0 15px;
    margin: 0 auto 25px auto;
    opacity: 0;
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-fill-mode: both;
  }

  .instance-details {
    display: flex;
    align-items: center;
  }

  .instance-details p {
    padding-left: 15px;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    color: rgba(0, 0, 0, 0.5);
  }

  .instance-status {
    display: flex;
    align-items: center;
  }

  .instance-status p {
    color: black;
    padding-left: 15px;
  }

  .instance-delete {
    margin-left: auto;
  }

  .instance-delete button {
    background-color: #e34040;
    color: white;
    cursor: pointer;
    margin-right: 0;
  }
`;

export default StyledInstanceComponent;
