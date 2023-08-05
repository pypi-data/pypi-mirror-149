import React from 'react';
import moment from 'moment';
import styled from 'styled-components';

interface IFooter {
  className?: string;
}

const Footer = ({ className }: IFooter): JSX.Element => (
  <footer className={`footer ${className}`}>
    <p>
      @2008 - {moment().year()} Oxford Nanopore Technologies. All rights
      reserved
    </p>
  </footer>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledFooter = styled(Footer)`
  width: 100%;
  padding: 25px;
  text-align: center;
  box-sizing: border-box;
`;

export default StyledFooter;
