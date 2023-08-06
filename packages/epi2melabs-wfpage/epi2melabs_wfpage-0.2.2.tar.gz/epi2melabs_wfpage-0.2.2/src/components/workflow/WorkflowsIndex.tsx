import React, { useState } from 'react';
import styled from 'styled-components';
import StyledTabbedHeader from '../common/TabbedHeader';
import StyledWorkflowList from './WorkflowList';
import StyledInstanceList from '../instance/InstanceList';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowsList {
  className?: string;
}

const WorkflowsPanel = ({ className }: IWorkflowsList): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState(0);
  const tabs = [
    {
      body: 'Select workflow',
      onClick: () => setSelectedTab(0),
      element: (
        <div className="tab-contents">
          <StyledWorkflowList />
        </div>
      )
    },
    {
      body: 'Workflow history',
      onClick: () => setSelectedTab(1),
      element: (
        <div className="tab-contents">
          <StyledInstanceList />
        </div>
      )
    }
  ];

  return (
    <div className={`index-panel ${className}`}>
      <StyledTabbedHeader
        title="EPI2ME Labs Workflows"
        body={
          <p className="large">
            EPI2ME Labs is developing nextflow workflows covering a variety
            everyday bioinformatics needs. These workflows are free and open to
            to be used by anyone.
          </p>
        }
        active={selectedTab}
        tabs={tabs}
      />

      {tabs[selectedTab].element}
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowsPanel = styled(WorkflowsPanel)`
  && {
    background-color: #f6f6f6;
    padding-bottom: 50px;
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
    opacity: 0;
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-fill-mode: both;
  }
`;

export default StyledWorkflowsPanel;
