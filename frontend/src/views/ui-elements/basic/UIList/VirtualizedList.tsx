'use client';

// material-ui
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';

// third party
import { List, RowComponentProps } from 'react-window';

// list render
function RowComponent({ index, style }: RowComponentProps) {
  return (
    <ListItemButton style={style} key={index}>
      <ListItemText primary={`Item ${index + 1}`} />
    </ListItemButton>
  );
}

// ================================|| UI LIST - SCROLLABLE ||================================ //

export default function VirtualizedList() {
  return <List rowComponent={RowComponent} rowProps={{ style: {} }} style={{ height: 280, width: '100%' }} rowCount={200} rowHeight={46} />;
}
