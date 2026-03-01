'use client';

// material-ui
import { styled } from '@mui/material/styles';

const ExperimentalStyled = styled('div')(({ theme }) => ({
  // hide license message
  '& .fc-license-message': {
    display: 'none'
  },

  // basic style
  '& .fc': {
    '--fc-bg-event-opacity': 1,
    '--fc-border-color': theme.vars.palette.divider,
    '--fc-daygrid-event-dot-width': '10px',
    '--fc-list-event-dot-width': '10px',
    '--fc-event-border-color': theme.vars.palette.primary.dark,
    '--fc-now-indicator-color': theme.vars.palette.error.main,
    color: theme.vars.palette.text.primary,
    fontFamily: theme.typography.fontFamily,
    '--fc-today-bg-color': theme.vars.palette.primary.light,
    ...theme.applyStyles('dark', {
      '--fc-today-bg-color': theme.vars.palette.dark[800]
    })
  },

  // date text
  '& .fc .fc-daygrid-day-top': {
    display: 'grid',
    '& .fc-daygrid-day-number': {
      textAlign: 'center',
      marginTop: 12,
      marginBottom: 12
    }
  },

  // weekday
  '& .fc .fc-col-header-cell': {
    backgroundColor: theme.vars.palette.grey[50],
    ...theme.applyStyles('dark', {
      backgroundColor: theme.vars.palette.dark.main
    })
  },

  '& .fc .fc-col-header-cell-cushion': {
    color: theme.vars.palette.grey[900],
    padding: 16
  },
  '& .fc-theme-standard .fc-list': {
    overflowX: 'auto'
  },

  // events
  '& .fc-direction-ltr .fc-daygrid-event.fc-event-end, .fc-direction-rtl .fc-daygrid-event.fc-event-start': {
    marginLeft: 4,
    marginBottom: 6,
    borderRadius: '6px'
  },

  '& .fc-direction-ltr .fc-daygrid-event.fc-event-start, .fc-direction-rtl .fc-daygrid-event.fc-event-end': {
    marginLeft: 4,
    marginBottom: 6,
    borderRadius: '6px'
  },

  '& .fc-h-event .fc-event-main': {
    padding: 4,
    paddingLeft: 8
  },

  // popover when multiple events
  '& .fc .fc-more-popover': {
    border: 'none',
    borderRadius: '14px'
  },

  '& .fc .fc-more-popover .fc-popover-body': {
    backgroundColor: theme.vars.palette.grey[200],
    ...theme.applyStyles('dark', {
      backgroundColor: theme.vars.palette.dark[800]
    }),
    borderBottomLeftRadius: '12px',
    borderBottomRightRadius: '12px'
  },

  '& .fc .fc-popover-header': {
    padding: 12,
    borderTopLeftRadius: '12px',
    borderTopRightRadius: '12px',
    backgroundColor: theme.vars.palette.grey[200],
    color: theme.vars.palette.text.primary,
    ...theme.applyStyles('dark', {
      backgroundColor: theme.vars.palette.dark[800],
      color: theme.vars.palette.dark.light
    })
  },

  // agenda view
  '& .fc-theme-standard .fc-list-day-cushion': {
    backgroundColor: theme.vars.palette.grey[100],
    ...theme.applyStyles('dark', {
      backgroundColor: theme.vars.palette.dark.main
    })
  },

  '& .fc .fc-list-event:hover td': {
    backgroundColor: theme.vars.palette.grey[100],
    ...theme.applyStyles('dark', {
      backgroundColor: theme.vars.palette.dark[800]
    })
  },

  '& .fc-timegrid-event-harness-inset .fc-timegrid-event, .fc-timegrid-event.fc-event-mirror, .fc-timegrid-more-link': {
    padding: 8,
    margin: 2
  }
}));

export default ExperimentalStyled;
