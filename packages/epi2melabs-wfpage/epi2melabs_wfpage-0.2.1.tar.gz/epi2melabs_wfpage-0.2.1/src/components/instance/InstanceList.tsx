import React, { useEffect, useState } from 'react';
import StyledStatusIndicator from './StatusIndicator';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { Instance } from './types';
import StyledEmptyPanel from '../common/EmptyPanel';
import { faHistory } from '@fortawesome/free-solid-svg-icons';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IInstanceList {
  className?: string;
  onlyTracked?: boolean;
}

const InstanceList = ({
  className,
  onlyTracked
}: IInstanceList): JSX.Element => {
  const [instances, setInstances] = useState<Instance[]>([]);
  const [trackedInstances, setTrackedInstances] = useState<Instance[]>([]);

  // ------------------------------------
  // Handle instance initialisation
  // ------------------------------------
  const getInstances = async () => {
    const instances = await requestAPI<any>('instances');
    const instanceList: Instance[] = Object.values(instances);
    const trackedInstanceList = instanceList.filter((I: Instance) =>
      ['UNKNOWN', 'LAUNCHED'].includes(I.status)
    );

    setInstances(instanceList);
    setTrackedInstances(trackedInstanceList);
  };

  useEffect(() => {
    getInstances();
  }, []);

  // ------------------------------------
  // Handle updating instances
  // ------------------------------------
  // Note: this should be changed to a single get request
  const updateTrackedInstances = async () => {
    const tracked = await Promise.all(
      trackedInstances.map(async I => {
        return await requestAPI<any>(`instances/${I.id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
      })
    );
    setTrackedInstances(tracked);
  };

  useEffect(() => {
    const insMonitor = setInterval(() => updateTrackedInstances(), 5000);
    return () => {
      clearInterval(insMonitor);
    };
  }, [trackedInstances]);

  // ------------------------------------
  // Handle displaying instances
  // ------------------------------------
  const formatDatetime = (datetime: string) => {
    const elements = datetime.split('-');
    const date = elements.slice(0, -2).join('/');
    const time = elements.slice(-2).join(':');
    return `${date} at ${time}`;
  };

  const sortInstances = (a: Instance, b: Instance) => {
    if (a.created_at < b.created_at) {
      return 1;
    }
    if (a.created_at > b.created_at) {
      return -1;
    }
    return 0;
  };

  const visibleInstances = onlyTracked ? trackedInstances : instances;
  const sortedVisibleInstances = visibleInstances.sort(sortInstances);

  if (sortedVisibleInstances.length === 0) {
    return (
      <div className={`instance-list ${className}`}>
        <StyledEmptyPanel
          body="There is no workflow history to display"
          icon={faHistory}
        />
      </div>
    );
  }

  return (
    <div className={`instance-list ${className}`}>
      <ul>
        {sortedVisibleInstances.map((Instance: Instance) => (
          <li>
            <div className="instance">
              <Link className="instance-link" to={`/instances/${Instance.id}`}>
                <div className="instance-details">
                  <div className="instance-name">
                    <p className="preheader">ID: {Instance.id}</p>
                    <h3 className="large">{Instance.name}</h3>
                  </div>
                  <div className="instance-created">
                    <p className="preheader">Created date</p>
                    <h4>{formatDatetime(Instance.created_at)}</h4>
                  </div>
                  <div className="instance-status-indicator">
                    <div className="instance-status">
                      <StyledStatusIndicator status={Instance.status} />
                      <p className="preheader">{Instance.status}</p>
                    </div>
                  </div>
                </div>
              </Link>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledInstanceList = styled(InstanceList)`
  && {
    width: calc(1024px + 30px);
    padding: 0 15px 15px 15px;
    margin: 0 auto;
    box-sizing: border-box;
  }

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .instance {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  .instance-details {
    padding: 25px 25px 25px 25px;
  }

  .instance-details p {
    padding: 0 0 5px 0;
    color: #ccc;
  }

  .instance-name,
  .instance-created {
    padding: 0 0 10px 0;
    margin: 0 0 15px 0;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-bottom: 1px solid #f2f2f2;
  }

  .instance-status {
    display: flex;
    align-items: center;
  }

  .instance-status p {
    padding: 0 0 0 15px;
  }
`;

export default StyledInstanceList;
