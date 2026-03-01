// material-ui
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import MainCard from 'ui-component/cards/MainCard';
import SecondaryAction from 'ui-component/cards/CardSecondaryAction';
import { gridSpacing } from 'store/constant';

// assets
import CloseIcon from '@mui/icons-material/Close';

// ===============================|| UI ALERT ||=============================== //

export default function UIAlert() {
  return (
    <MainCard title="Alert" secondary={<SecondaryAction link="https://next.material-ui.com/components/alert/" />}>
      <Stack sx={{ gap: gridSpacing }}>
        <SubCard title="Basic">
          <Stack sx={{ gap: 2 }}>
            <Alert icon={false} severity="primary">
              This is primary alert!
            </Alert>
            <Alert icon={false} severity="error">
              This is error alert!
            </Alert>
            <Alert icon={false} severity="warning">
              This is warning alert!
            </Alert>
            <Alert icon={false} severity="success">
              This is success alert!
            </Alert>
            <Alert icon={false} severity="info">
              This is info alert!
            </Alert>
          </Stack>
        </SubCard>
        <SubCard title="Description Alert">
          <Stack sx={{ gap: 2 }}>
            <Alert severity="primary" icon={false}>
              <AlertTitle>Primary</AlertTitle>
              This is an primary alert — <strong>check it out!</strong>
            </Alert>
            <Alert severity="error" icon={false}>
              <AlertTitle>Error</AlertTitle>
              This is an error alert — <strong>check it out!</strong>
            </Alert>
            <Alert severity="warning" icon={false}>
              <AlertTitle>Warning</AlertTitle>
              This is a warning alert — <strong>check it out!</strong>
            </Alert>
            <Alert severity="info" icon={false}>
              <AlertTitle>Info</AlertTitle>
              This is an info alert — <strong>check it out!</strong>
            </Alert>
            <Alert severity="success" icon={false}>
              <AlertTitle>Success</AlertTitle>
              This is a success alert — <strong>check it out!</strong>
            </Alert>
          </Stack>
        </SubCard>
        <SubCard title="Alert with Action">
          <Stack sx={{ gap: 2 }}>
            <Alert
              severity="primary"
              icon={false}
              action={
                <>
                  <Button color="inherit" size="small">
                    UNDO
                  </Button>
                  <IconButton size="small" aria-label="close" color="inherit">
                    <CloseIcon fontSize="small" />
                  </IconButton>
                </>
              }
            >
              This is primary alert!
            </Alert>
            <Alert
              severity="error"
              icon={false}
              action={
                <>
                  <Button color="inherit" size="small">
                    UNDO
                  </Button>
                  <IconButton size="small" aria-label="close" color="inherit">
                    <CloseIcon fontSize="small" />
                  </IconButton>
                </>
              }
            >
              This is error alert!
            </Alert>
            <Alert
              severity="warning"
              icon={false}
              action={
                <>
                  <Button color="inherit" size="small">
                    UNDO
                  </Button>
                  <IconButton size="small" aria-label="close" color="inherit">
                    <CloseIcon fontSize="small" />
                  </IconButton>
                </>
              }
            >
              This is warning alert!
            </Alert>
            <Alert
              severity="success"
              icon={false}
              action={
                <>
                  <Button color="inherit" size="small">
                    UNDO
                  </Button>
                  <IconButton size="small" aria-label="close" color="inherit">
                    <CloseIcon fontSize="small" />
                  </IconButton>
                </>
              }
            >
              This is success alert!
            </Alert>
            <Alert
              severity="info"
              icon={false}
              action={
                <>
                  <Button color="inherit" size="small">
                    UNDO
                  </Button>
                  <IconButton size="small" aria-label="close" color="inherit">
                    <CloseIcon fontSize="small" />
                  </IconButton>
                </>
              }
            >
              This is info alert!
            </Alert>
          </Stack>
        </SubCard>
        <SubCard title="Alert with Icon">
          <Stack sx={{ gap: 2 }}>
            <Alert severity="primary">This is primary alert!</Alert>
            <Alert severity="error">This is error alert!</Alert>
            <Alert severity="warning">This is warning alert!</Alert>
            <Alert severity="success">This is success alert!</Alert>
            <Alert severity="info">This is info alert!</Alert>
          </Stack>
        </SubCard>
        <SubCard title="Outline Alert">
          <Stack sx={{ gap: 2 }}>
            <Alert variant="outlined" severity="primary">
              This is an primary alert — check it out!
            </Alert>
            <Alert variant="outlined" severity="error">
              This is an error alert — check it out!
            </Alert>
            <Alert variant="outlined" severity="warning">
              This is a warning alert — check it out!
            </Alert>
            <Alert variant="outlined" severity="info">
              This is an info alert — check it out!
            </Alert>
            <Alert variant="outlined" severity="success">
              This is a success alert — check it out!
            </Alert>
          </Stack>
        </SubCard>
        <SubCard title="Filled Alert">
          <Stack sx={{ gap: 2 }}>
            <Alert variant="filled" severity="primary">
              This is an primary alert — check it out!
            </Alert>
            <Alert variant="filled" severity="error">
              This is an error alert — check it out!
            </Alert>
            <Alert variant="filled" severity="warning">
              This is a warning alert — check it out!
            </Alert>
            <Alert variant="filled" severity="info">
              This is an info alert — check it out!
            </Alert>
            <Alert variant="filled" severity="success">
              This is a success alert — check it out!
            </Alert>
          </Stack>
        </SubCard>
      </Stack>
    </MainCard>
  );
}
