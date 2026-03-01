'use client';

import { useState } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';

// third party
import { Droppable, Draggable } from '@hello-pangea/dnd';

// project imports
import useConfig from 'hooks/useConfig';
import EditColumn from './EditColumn';
import Items from './Items';
import AddItem from './AddItem';
import AlertColumnDelete from './AlertColumnDelete';
import { gridSpacing } from 'store/constant';
import { openSnackbar } from 'store/slices/snackbar';
import { useDispatch, useSelector } from 'store';
import { deleteColumn } from 'store/slices/kanban';
import { withAlpha } from 'utils/colorUtils';

// assets
import DeleteTwoToneIcon from '@mui/icons-material/DeleteTwoTone';

// types
import { DefaultRootStateProps } from 'types';
import { KanbanColumn } from 'types/kanban';

interface Props {
  column: KanbanColumn;
  index: number;
}

// ==============================|| KANBAN BOARD - COLUMN ||============================== //

export default function Columns({ column, index }: Props) {
  const theme = useTheme();
  const dispatch = useDispatch();

  const {
    state: { borderRadius }
  } = useConfig();
  const { items, columns, columnsOrder } = useSelector((state: DefaultRootStateProps) => state.kanban);
  const columnItems = column.itemIds.map((itemId) => items.filter((item) => item.id === itemId)[0]);

  const handleColumnDelete = () => {
    setOpen(true);
  };

  const [open, setOpen] = useState(false);
  const handleClose = (status: boolean) => {
    setOpen(false);
    if (status) {
      dispatch(deleteColumn(column.id, columnsOrder, columns));
      dispatch(
        openSnackbar({
          open: true,
          message: 'Column deleted successfully',
          anchorOrigin: { vertical: 'top', horizontal: 'right' },
          variant: 'alert',
          alert: {
            color: 'success'
          },
          close: false
        })
      );
    }
  };

  return (
    <Draggable draggableId={column.id} index={index}>
      {(provided, snapshot) => (
        <Box
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          sx={{
            minWidth: 250,
            border: '1px solid',
            borderRadius: `${borderRadius}px`,
            userSelect: 'none',
            margin: `0 ${16}px 0 0`,
            height: '100%',
            ...provided.draggableProps.style,
            borderColor: withAlpha(theme.vars.palette.primary[200], 0.75),
            bgcolor: snapshot.isDragging ? theme.vars.palette.grey[50] : theme.vars.palette.primary.light,

            ...theme.applyStyles('dark', {
              borderColor: theme.vars.palette.background.default,
              bgcolor: snapshot.isDragging ? theme.vars.palette.grey[50] : theme.vars.palette.background.default
            })
          }}
        >
          <Droppable droppableId={column.id} type="item">
            {(providedDrop, snapshotDrop) => (
              <Box
                ref={providedDrop.innerRef}
                {...providedDrop.droppableProps}
                sx={{
                  padding: '8px 16px 14px',
                  width: 'auto',
                  borderRadius: `${borderRadius}px`,
                  background: snapshotDrop.isDraggingOver ? theme.vars.palette.primary[200] : theme.vars.palette.primary.light,

                  ...theme.applyStyles('dark', {
                    background: snapshotDrop.isDraggingOver ? theme.vars.palette.text.disabled : theme.vars.palette.background.default
                  })
                }}
              >
                <Grid container spacing={gridSpacing} sx={{ alignItems: 'center' }}>
                  <Grid size="grow">
                    <EditColumn column={column} />
                  </Grid>
                  <Grid sx={{ mb: 1.5 }}>
                    <IconButton onClick={handleColumnDelete} size="large" aria-label="Delete Columns">
                      <DeleteTwoToneIcon fontSize="small" aria-controls="menu-simple-card" aria-haspopup="true" />
                    </IconButton>
                    {open && <AlertColumnDelete title={column.title} open={open} handleClose={handleClose} />}
                  </Grid>
                </Grid>
                {columnItems.map((item, i) => (
                  <Items key={i} item={item} index={i} />
                ))}
                {providedDrop.placeholder}
                <AddItem columnId={column.id} />
              </Box>
            )}
          </Droppable>
        </Box>
      )}
    </Draggable>
  );
}
