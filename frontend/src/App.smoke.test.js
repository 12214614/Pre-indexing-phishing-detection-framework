import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

test('App renders and unmounts without crashing', () => {
  const container = document.createElement('div');
  const root = createRoot(container);

  root.render(<App />);
  root.unmount();
});
