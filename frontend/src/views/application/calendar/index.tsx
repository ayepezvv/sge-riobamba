'use client';

import { useEffect, useRef, useState } from 'react';

// material-ui
import { Theme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';

// third party
import FullCalendar from '@fullcalendar/react';
import listPlugin from '@fullcalendar/list';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import timelinePlugin from '@fullcalendar/timeline';
import { EventDropArg, EventClickArg, DateSelectArg } from '@fullcalendar/core';
import interactionPlugin, { EventResizeDoneArg } from '@fullcalendar/interaction';

import { FormikValues } from 'formik';

// project imports
import Toolbar from './Toolbar';
import AddEventForm from './AddEventForm';
import CalendarStyled from './CalendarStyled';

import Loader from 'ui-component/Loader';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';

import { dispatch, useSelector } from 'store';
import { getEvents, addEvent, updateEvent, removeEvent } from 'store/slices/calendar';

// assets
import AddAlarmTwoToneIcon from '@mui/icons-material/AddAlarmTwoTone';

// types
import { DateRange } from 'types';

// ==============================|| APPLICATION CALENDAR ||============================== //

export default function Calendar() {
  const calendarRef = useRef<FullCalendar>(null);
  const matchSm = useMediaQuery((theme: Theme) => theme.breakpoints.down('md'));

  const [loading, setLoading] = useState(true);

  // pull events from redux
  const { events } = useSelector((state) => state.calendar);

  useEffect(() => {
    dispatch(getEvents()).then(() => setLoading(false));
  }, []);

  const [date, setDate] = useState(new Date());
  const [view, setView] = useState(matchSm ? 'listWeek' : 'dayGridMonth');

  // modal state
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedRange, setSelectedRange] = useState<DateRange | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<FormikValues | null>(null);

  // toolbar handlers
  const handleDateToday = () => {
    const calendarEl = calendarRef.current?.getApi();
    calendarEl?.today();
    setDate(calendarEl?.getDate() ?? new Date());
  };

  const handleViewChange = (newView: string) => {
    const calendarEl = calendarRef.current?.getApi();
    calendarEl?.changeView(newView);
    setView(newView);
  };

  useEffect(() => {
    handleViewChange(matchSm ? 'listWeek' : 'dayGridMonth');
  }, [matchSm]);

  const handleDatePrev = () => {
    const calendarEl = calendarRef.current?.getApi();
    calendarEl?.prev();
    setDate(calendarEl?.getDate() ?? new Date());
  };

  const handleDateNext = () => {
    const calendarEl = calendarRef.current?.getApi();
    calendarEl?.next();
    setDate(calendarEl?.getDate() ?? new Date());
  };

  // calendar event select/add/edit/delete
  const handleRangeSelect = (arg: DateSelectArg) => {
    calendarRef.current?.getApi().unselect();
    setSelectedRange({ start: arg.start, end: arg.end });
    setSelectedEvent(null);
    setIsModalOpen(true);
  };

  const handleEventSelect = (arg: EventClickArg) => {
    const found = events.find((e) => e.id === arg.event.id);
    setSelectedEvent(found ?? null);
    setSelectedRange(null);
    setIsModalOpen(true);
  };

  const handleEventUpdate = ({ event }: EventResizeDoneArg | EventDropArg) => {
    dispatch(
      updateEvent({
        id: event.id,
        title: event.title,
        allDay: event.allDay,
        start: event.start ? event.start.toISOString() : undefined,
        end: event.end ? event.end.toISOString() : undefined
      })
    );
  };

  // modal actions
  const handleEventCreate = (data: FormikValues) => {
    const payload = {
      ...data,
      start: data.start instanceof Date ? data.start.toISOString() : data.start,
      end: data.end instanceof Date ? data.end.toISOString() : data.end
    };
    dispatch(addEvent(payload));
    handleModalClose();
  };

  const handleUpdateEvent = (eventId: string, update: FormikValues) => {
    const payload = {
      id: eventId,
      ...update,
      start: update.start instanceof Date ? update.start.toISOString() : update.start,
      end: update.end instanceof Date ? update.end.toISOString() : update.end
    };
    dispatch(updateEvent(payload));
    handleModalClose();
  };

  const handleEventDelete = (id: string) => {
    dispatch(removeEvent(id));
    handleModalClose();
  };

  const handleAddClick = () => {
    setSelectedEvent(null);
    setSelectedRange(null);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedEvent(null);
    setSelectedRange(null);
  };

  if (loading) return <Loader />;

  return (
    <MainCard
      title="Event Calendar"
      secondary={
        <Button color="secondary" variant="contained" onClick={handleAddClick}>
          <AddAlarmTwoToneIcon fontSize="small" sx={{ mr: 0.75 }} />
          Add New Event
        </Button>
      }
    >
      <CalendarStyled>
        <Toolbar
          date={date}
          view={view}
          onClickNext={handleDateNext}
          onClickPrev={handleDatePrev}
          onClickToday={handleDateToday}
          onChangeView={handleViewChange}
        />
        <SubCard>
          <FullCalendar
            ref={calendarRef}
            plugins={[listPlugin, dayGridPlugin, timelinePlugin, timeGridPlugin, interactionPlugin]}
            initialView={view}
            initialDate={date}
            events={events}
            selectable
            editable
            droppable
            weekends
            height={matchSm ? 'auto' : 720}
            headerToolbar={false}
            allDayMaintainDuration
            eventResizableFromStart
            select={handleRangeSelect}
            eventDrop={handleEventUpdate}
            eventClick={handleEventSelect}
            eventResize={handleEventUpdate}
            eventTimeFormat={{ hour: 'numeric', minute: '2-digit', meridiem: 'short' }}
          />
        </SubCard>
      </CalendarStyled>

      {/* Dialog renders its body even if not open */}
      <Dialog maxWidth="sm" fullWidth onClose={handleModalClose} open={isModalOpen} slotProps={{ paper: { sx: { p: 0 } } }}>
        {isModalOpen && (
          <AddEventForm
            event={selectedEvent}
            range={selectedRange}
            onCancel={handleModalClose}
            handleDelete={handleEventDelete}
            handleCreate={handleEventCreate}
            handleUpdate={handleUpdateEvent}
          />
        )}
      </Dialog>
    </MainCard>
  );
}
