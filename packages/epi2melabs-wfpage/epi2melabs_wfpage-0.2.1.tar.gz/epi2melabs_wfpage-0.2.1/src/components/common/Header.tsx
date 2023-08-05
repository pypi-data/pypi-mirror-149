import React from 'react';
import { logoSVG } from '../../asset';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHouse } from '@fortawesome/free-solid-svg-icons';

export const LabsLogo = (): JSX.Element => {
  const logoSVGBlob = new Blob([logoSVG], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(logoSVGBlob);

  return (
    <div className="labsLogo">
      <img src={url} alt="The EPI2ME Labs logo" />
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IHeader {
  className?: string;
}

const Header = ({ className }: IHeader): JSX.Element => (
  <header className={`header ${className}`}>
    <div className="header-contents">
      <Link className="header-logo" to="/">
        <LabsLogo />
      </Link>
      <div className="header-links">
        <ul>
          <li className="text-link">
            <Link to="/workflows">Workflows</Link>
          </li>
          <li className="text-link">
            <Link to="/notebooks">Notebooks</Link>
          </li>
          <li>
            <Link to="/">
              <FontAwesomeIcon icon={faHouse} />
            </Link>
          </li>
        </ul>
      </div>
    </div>
  </header>
);

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledHeader = styled(Header)`
  padding: 15px 25px;
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  background-color: #00485b;
  color: white;
  box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
  z-index: 2000;

  .header-contents {
    max-width: 1024px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
  }

  .header-links {
    display: flex;
  }

  .header-links ul {
    display: flex;
    align-items: center;
  }

  .header-links a {
    margin: 0 0 0 20px;
    outline: none;
    background: none;
    border: none;
    vertical-align: middle;
    cursor: pointer;
  }

  .header-links .text-link a {
    color: white;
    font-size: 13px;
    font-weight: 500;
  }

  .header-links a svg {
    font-size: 1.2em;
    color: rgba(255, 255, 255, 0.35);
  }

  .header-links a:hover svg {
    color: rgba(255, 255, 255, 0.85);
  }

  .labsLogo {
    display: flex;
  }

  .labsLogo img {
    width: 25px;
  }

  a {
    font-weight: bold;
  }
`;

export default StyledHeader;
