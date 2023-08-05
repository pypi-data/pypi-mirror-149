import React from 'react';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
export interface ITabbedHeaderTab {
  body: string;
  className?: string;
  onClick: CallableFunction;
  element?: React.ReactNode;
}

interface ITabbedHeader {
  className?: string;
  title: string;
  body: React.ReactNode;
  active: number;
  tabs: ITabbedHeaderTab[];
}

const TabbedHeader = ({
  className,
  title,
  body,
  active,
  tabs
}: ITabbedHeader): JSX.Element => (
  <div className={`header-title ${className}`}>
    <div className="header-title-contents">
      <h1>{title}</h1>
      {body}
      <ul className="header-title-tabs">
        {tabs.map((Item, idx) => (
          <li
            className={`header-title-workflows-link ${
              idx === active ? 'active' : ''
            } ${Item.className || ''}`}
          >
            <button onClick={() => Item.onClick()}>{Item.body}</button>
          </li>
        ))}
      </ul>
    </div>
  </div>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledHeaderTitle = styled(TabbedHeader)`
  && {
    max-width: 100%;
    padding: 50px 25px;
    margin: 0 0 50px 0;
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: flex-start;
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
  }

  .header-title-contents {
    width: 100%;
    max-width: 1024px;
    text-align: left;
  }

  .header-title-contents h1 {
    padding: 0 0 25px 0;
  }

  .header-title-contents p {
    max-width: 800px;
  }

  .header-title-tabs {
    padding: 35px 0 5px 0;
    display: flex;
  }

  .header-title-tabs button {
    margin-right: 15px;
    padding: 12px 24px;
    border-radius: 4px;
    border: none;
    display: block;
    font-weight: 500;
    font-size: 13px;
    line-height: 1em;
    transition: 0.2s ease-in-out all;
    background-color: #eee;
    cursor: pointer;
  }

  .header-title-tabs .active button {
    color: white;
    background-color: #00485b;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
  }
`;

export default StyledHeaderTitle;
