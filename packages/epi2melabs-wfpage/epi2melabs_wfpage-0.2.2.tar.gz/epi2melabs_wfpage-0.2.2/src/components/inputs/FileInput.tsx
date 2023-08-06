import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faFolder,
  faFile,
  faTimes,
  faLevelUpAlt
} from '@fortawesome/free-solid-svg-icons';
import { requestAPI } from '../../handler';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Type definitions
// -----------------------------------------------------------------------------
export const FILE_INPUT = 'file';
export const DIR_INPUT = 'dir';
export const PATH_INPUT = 'path';

export interface IFileSettings {
  id: string;
  label: string;
  format: string;
  description: string;
  defaultValue?: string;
  pattern?: string;
}

interface IFileInput extends IFileSettings {
  error: string[];
  onChange: CallableFunction;
  className?: string;
}

interface IPath {
  name: string;
  path: string;
  updated: string;
  isdir: boolean;
}

// -----------------------------------------------------------------------------
// Helper methods
// -----------------------------------------------------------------------------
const setNativeValue = (element: any, value: any) => {
  const valueSetter = Object.getOwnPropertyDescriptor(element, 'value')?.set;
  const prototype = Object.getPrototypeOf(element);
  const prototypeValueSetter = Object.getOwnPropertyDescriptor(
    prototype,
    'value'
  )?.set;

  if (valueSetter && valueSetter !== prototypeValueSetter) {
    prototypeValueSetter?.call(element, value);
  } else {
    valueSetter?.call(element, value);
  }
};

const mapFormatToEndpoint = (format: string) => {
  let fmt;
  switch (format) {
    case 'file-path':
      fmt = 'file';
      break;
    case 'directory-path':
      fmt = 'directory';
      break;
    default:
      fmt = 'path';
  }
  return fmt;
};

const getDirContents = async (path: string) => {
  const encodedPath = encodeURIComponent(path);
  const data = await requestAPI<any>(`directory/${encodedPath}?contents=true`, {
    method: 'GET'
  });
  return data.contents;
};

const getParentDir = (path: string) => {
  const parent = path.split('/').slice(0, -1).join('/');
  if (parent === '') {
    return '/';
  }
  return parent;
};

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
const FileInput = ({
  id,
  label,
  format,
  description,
  defaultValue,
  pattern,
  error,
  onChange,
  className
}: IFileInput) => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const [selectedPath, setSelectedPath] = useState<string>('');
  const [browserError, setBrowserError] = useState<string | null>(null);
  const [browserLocation, setBrowserLocation] = useState<string>('/');
  const [browserContents, setBrowserContents] = useState<IPath[]>([]);
  const [browserOpen, setBrowserOpen] = useState(false);
  const inputRef = useRef(null);

  const mappedFormat = mapFormatToEndpoint(format);

  let errors: string[] = [];
  if (error.length) {
    errors = [...error];
  }
  if (browserError) {
    errors = [browserError, ...errors];
  }

  // ------------------------------------
  // Handle browser change
  // ------------------------------------
  useEffect(() => {
    const update = async () => {
      const contents = await getDirContents(browserLocation);
      if (contents) {
        setBrowserContents(
          contents
            .filter((Item: IPath) =>
              mappedFormat === 'directory' && !Item.isdir ? false : true
            )
            .sort((a: IPath, b: IPath) => a.name.localeCompare(b.name))
        );
      }
    };
    update();
  }, [browserLocation]);

  const handleDoubleClickPath = (path: string, dir: boolean) => {
    if (dir) {
      setBrowserLocation(path);
    }
  };

  // ------------------------------------
  // Handle input change
  // ------------------------------------
  const handleInputChange = (value: any) => {
    const fmt = mapFormatToEndpoint(format);
    validatePath(value, fmt);
  };

  const handleClickPath = (path: string, dir: boolean, ref: any) => {
    if (path === selectedPath) {
      return;
    }
    if (!dir && mappedFormat === 'directory') {
      return;
    }
    if (dir && mappedFormat === 'file') {
      return;
    }
    setSelectedPath(path);
    const current = ref.current;
    if (current) {
      setNativeValue(current, path);
      const event = new Event('input', { bubbles: true });
      current.dispatchEvent(event);
    }
  };

  // ------------------------------------
  // Handle path validation
  // ------------------------------------
  const validatePath = async (path: string, format: string) => {
    if (
      [/http:\/\//, /https:\/\//, /^$/, /s3:\/\//].some(rx => rx.test(path))
    ) {
      setBrowserError(null);
      onChange(id, format, path);
      return;
    }
    const encodedPath = encodeURIComponent(path);
    const data = await requestAPI<any>(`${format}/${encodedPath}`, {
      method: 'GET'
    });
    if (!data.exists) {
      setBrowserError(data.error);
      onChange(id, format, '');
      return;
    }
    setBrowserError(null);
    onChange(id, format, path);
  };

  return (
    <div id={id} className={`FileInput ${className}`}>
      <h4>{label}</h4>
      <p>{description}</p>
      <div className="file-input-container">
        <label htmlFor={id}>
          <input
            id={id}
            ref={inputRef}
            type="text"
            placeholder={'Enter a value'}
            defaultValue={defaultValue}
            pattern={pattern}
            onChange={e => {
              handleInputChange(e.target.value);
            }}
          />
        </label>
        <button
          className="file-browser-toggle"
          onClick={() => setBrowserOpen(!browserOpen)}
        >
          Browse
        </button>
      </div>

      {browserOpen ? (
        <div className="file-browser">
          <div className="file-browser-contents">
            <div className="file-browser-path file-browser-close">
              <button onClick={() => setBrowserOpen(false)}>
                <FontAwesomeIcon icon={faTimes} />
                {selectedPath.length ? 'Close' : 'Select'}
              </button>
            </div>
            <ul>
              {browserLocation !== '/' ? (
                <li className="file-browser-path file-browser-back">
                  <button
                    onClick={() =>
                      setBrowserLocation(getParentDir(browserLocation))
                    }
                  >
                    <FontAwesomeIcon icon={faLevelUpAlt} />
                    Go Up
                  </button>
                </li>
              ) : (
                ''
              )}
              {browserContents.map(Item => (
                <li
                  className={`file-browser-path ${
                    selectedPath === Item.path ? 'selected' : ''
                  }`}
                >
                  <button
                    onClick={() =>
                      handleClickPath(Item.path, Item.isdir, inputRef)
                    }
                    onDoubleClick={() =>
                      handleDoubleClickPath(Item.path, Item.isdir)
                    }
                  >
                    <FontAwesomeIcon icon={Item.isdir ? faFolder : faFile} />
                    {Item.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      ) : (
        ''
      )}
      {errors.length ? (
        <div className="error">
          {errors.map(Err => (
            <p>Error: {Err}</p>
          ))}
        </div>
      ) : (
        ''
      )}
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledFileInput = styled(FileInput)`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  .file-input-container {
    display: flex;
    color: #212529;
    border-radius: 4px;
    border: 1px solid rgba(0, 0, 0, 0.125);
    background-color: #f8f9fa;
  }

  .file-input-container:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  label {
    width: 100%;
    display: flex;
  }

  input {
    display: block;
    width: 100%;
    box-sizing: border-box;
  }

  input,
  .file-browser-toggle {
    margin: 0;
    padding: 15px 25px;

    font-size: 14px;
    line-height: 1em;

    color: #212529;
    border: 0;
    background-color: transparent;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  .file-browser-toggle {
    line-height: 1.2em;
    border-radius: 0;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    background-color: rgba(0, 0, 0, 0.125);
    color: #333;
    cursor: pointer;
  }

  .file-browser-toggle:hover {
    background-color: #005c75;
    color: white;
  }

  .file-browser {
    position: fixed;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    top: 0px;
    left: 0px;
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.35);
    /* max-height: 300px; */
    /* margin: 10px 0 0 0; */
    /* border-radius: 4px; */
    /* background-color: #f3f3f3; */
    /* overflow-y: auto; */
  }

  .file-browser-contents {
    width: 900px;
    /* max-height: 500px; */
    border-radius: 4px;
    overflow-y: auto;
    /* background-color: #f3f3f3; */
    background-color: rgba(255, 255, 255, 0.6);
  }

  .file-browser-contents > ul {
    max-height: 500px;
    overflow-y: auto;
  }

  .file-browser-path button {
    box-sizing: border-box;
    width: 100%;
    padding: 15px 25px;
    display: flex;
    align-items: center;
    text-align: left;
    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    outline: none;
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #f4f4f4;
    cursor: pointer;
  }

  .file-browser-path:nth-child(even) button {
    background-color: #f2f2f2;
  }

  .file-browser-path:last-child button {
    border-bottom: none;
  }

  .file-browser-path button:hover {
    color: #005c75;
  }

  .file-browser-path.selected button {
    background-color: #005c75;
    color: white;
  }

  .file-browser-path.selected button:hover {
    color: white;
  }

  .file-browser-back {
    font-style: italic;
    background-color: rgba(0, 0, 0, 0.1);
  }

  .file-browser-close {
    background-color: transparent;
  }

  .file-browser-path.file-browser-close button {
    display: flex;
    justify-content: end;
    border-radius: 0;
    border-bottom: 2px solid #ccc;
    color: #333;
  }

  .file-browser-path.file-browser-close:hover button {
    background-color: #f2f2f2;
    color: #333;
  }

  .file-browser-path button svg {
    padding: 0 10px 0 0;
    color: lightgray;
    font-size: 1.5em;
  }

  .file-browser-path button:hover svg {
    color: #005c75;
  }

  .file-browser-path.selected button:hover svg {
    color: lightgray;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;

export default StyledFileInput;
