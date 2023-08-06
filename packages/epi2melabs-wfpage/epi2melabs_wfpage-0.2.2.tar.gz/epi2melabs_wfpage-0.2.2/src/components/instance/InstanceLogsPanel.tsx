import React, { useEffect, useState } from 'react';
import StyledLoadingSpinner from '../common/LoadingSpinner';
import { finished } from './StatusIndicator';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { Instance } from './types';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IInstanceLogsPanel {
  className?: string;
  title: string;
  logfile: string;
  instanceData: Instance;
  instanceStatus: string;
}

const InstanceLogsPanel = ({
  className,
  title,
  logfile,
  instanceData,
  instanceStatus
}: IInstanceLogsPanel): JSX.Element => {
  const [instanceLogs, setInstanceLogs] = useState<string[] | null>(null);

  // ------------------------------------
  // Get instance params / logs / outputs
  // ------------------------------------
  const getInstanceLogs = async (
    instanceData: Instance | null,
    selectedLog: string
  ) => {
    if (instanceData) {
      const encodedPath = encodeURIComponent(
        `${instanceData.path}/${selectedLog}`
      );
      const { contents } = await requestAPI<any>(
        `file/${encodedPath}?contents=true`
      );
      if (contents !== null) {
        setInstanceLogs(contents);
      }
    }
  };

  // ------------------------------------
  // Monitor instance status
  // ------------------------------------
  useEffect(() => {
    getInstanceLogs(instanceData, logfile);
    if (finished.includes(instanceStatus)) {
      return;
    } else {
      const logsMonitor = setInterval(
        () => getInstanceLogs(instanceData, logfile),
        7500
      );
      return () => {
        getInstanceLogs(instanceData, logfile);
        clearInterval(logsMonitor);
      };
    }
  }, [instanceStatus, logfile]);

  return (
    <div className={`instance-logs ${className}`}>
      <div className="instance-logs-header">
        <h3>{title}</h3>
      </div>
      <div className="instance-logs-items">
        {instanceLogs && instanceLogs.length ? (
          <ul>
            {instanceLogs.map(Item => (
              <li>
                <p>{Item}</p>
              </li>
            ))}
          </ul>
        ) : (
          <div>
            <StyledLoadingSpinner />
          </div>
        )}
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledInstanceLogsPanel = styled(InstanceLogsPanel)`
  && {
    border-radius: 4px;
    padding: 25px;
    margin: 0 0 50px 0;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
  }

  .instance-logs-header {
    padding-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .instance-logs-items {
    max-height: 500px;
    overflow-y: scroll;
    padding: 15px;
    background-color: #f4f4f4;
    border-radius: 4px;
  }

  .instance-logs-items p {
    font-family: monospace;
  }
`;

export default StyledInstanceLogsPanel;
