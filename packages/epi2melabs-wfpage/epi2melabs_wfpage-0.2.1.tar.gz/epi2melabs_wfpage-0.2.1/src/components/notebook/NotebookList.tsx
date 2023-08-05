import React, { useState, useEffect } from 'react';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { Contents } from '@jupyterlab/services';
import styled from 'styled-components';
import moment from 'moment';
import StyledEmptyPanel from '../common/EmptyPanel';
import { faBookOpen, faBook } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const IPYNB = '.ipynb';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
export interface ITrackedNotebook {
  name: string;
  path: string;
  last_modified: string;
  onClick?: (e: string) => void;
}

const NotebooksList = ({
  path,
  onClick,
  docTrack,
  buttonText,
  className
}: {
  path: string;
  onClick: CallableFunction;
  docTrack: IDocumentManager;
  buttonText: string;
  className?: string;
}): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const [notebooks, setNotebooks] = useState<ITrackedNotebook[]>([]);

  const handleUpdateSections = async (path: string) => {
    setNotebooks(await getNotebooks(path, docTrack));
  };

  useEffect(() => {
    handleUpdateSections(path);
    const slotHandleUpdateSections = (e: any) => {
      handleUpdateSections(path);
    };

    const fileSignal = docTrack.services.contents.fileChanged;
    fileSignal.connect(slotHandleUpdateSections);
    return () => {
      fileSignal.disconnect(slotHandleUpdateSections);
    };
  }, [path]);

  // ------------------------------------
  // Notebook doctrack utilities
  // ------------------------------------
  const getFiles = async (
    path: string,
    docTrack: IDocumentManager
  ): Promise<Contents.IModel[]> => {
    return (
      await Promise.all<Contents.IModel>(
        (
          await docTrack.services.contents.get(path)
        ).content.map((Item: Contents.IModel) => {
          return Item.type === 'directory' ? null : Item;
        })
      )
    ).filter(Item => !!Item);
  };

  const getNotebooks = async (
    path: string,
    docTrack: IDocumentManager
  ): Promise<ITrackedNotebook[]> => {
    return (await getFiles(path, docTrack))
      .filter((Item: any) => Item.path.endsWith(IPYNB))
      .map(
        (Item: any): ITrackedNotebook => ({
          name: Item.name,
          path: Item.path,
          last_modified: Item.last_modified
        })
      );
  };

  // ------------------------------------
  // Handle formatting notebook entries
  // ------------------------------------
  const handleExtractName = (path: string): string => {
    return path
      .split('/')
      .reverse()[0]
      .split('_')
      .join(' ')
      .split('.ipynb')
      .join('');
  };

  const handleFormatUpdated = (modified: string): string => {
    return moment(modified).format('MMMM Do YYYY, h:mm:ss a');
  };

  if (notebooks.length === 0) {
    return (
      <div className={`notebooks-list ${className}`}>
        <StyledEmptyPanel
          body="There are no notebooks to display"
          icon={faBookOpen}
        />
      </div>
    );
  }

  return (
    <div className={`notebooks-list ${className}`}>
      <ul>
        {notebooks.map(Item => (
          <li>
            <div className="notebook">
              <button
                className="notebook-button"
                onClick={() => onClick(Item.path, docTrack)}
              >
                <div className="notebook-header">
                  <FontAwesomeIcon icon={faBook} />
                </div>
                <div className="notebook-details">
                  <div className="notebook-name">
                    <p className="preheader">Notebook name</p>
                    <h3 className="large">{handleExtractName(Item.path)}</h3>
                  </div>
                  <div className="notebook-modified">
                    <p className="preheader">Last modified</p>
                    <h4>{handleFormatUpdated(Item.last_modified)}</h4>
                  </div>
                </div>
              </button>
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
const StyledNotebooksList = styled(NotebooksList)`
  && {
    max-width: calc(1024px + 30px);
    padding: 0 15px 15px 15px;
    margin: 0 auto;
    box-sizing: border-box;
  }

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .notebook {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  .notebook-button {
    outline: none;
    border: none;
    background-color: transparent;
    cursor: pointer;
  }

  .notebook-header {
    box-sizing: border-box;
    width: 100%;
    padding: 25px 25px 0;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    border-radius: 4px;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }

  .notebook-header svg {
    padding: 15px 16px;
    border-radius: 50px;
    background-color: transparent;
    border: 2px solid #e65100;
    color: #e65100;
  }

  .notebook-details {
    padding: 25px 25px 25px 25px;
    text-align: left;
  }

  .notebook-details p {
    padding: 0 0 5px 0;
    color: #ccc;
  }

  .notebook-name {
    padding: 0 0 10px 0;
    margin: 0 0 15px 0;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-bottom: 1px solid #f2f2f2;
  }
`;

export default StyledNotebooksList;
