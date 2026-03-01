'use client';

import { useState } from 'react';

// material-ui
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// third party
import { StyleSpecification } from 'maplibre-gl';
import { RMap, RMarker, RPopup, RNavigationControl, markerPopupOffset } from 'maplibre-react-components';

// project imports
import SubCard from 'ui-component/cards/SubCard';
import osm_bright from './map-data/osm_bright.json';

type CountryProps = {
  name: string;
  capital: string;
  latlng: number[];
  timezones: string[];
  country_code: string;
};

interface Props {
  data: CountryProps[];
}

// ==============================|| MAPLIBRE - MARKERS AND POPUP ||============================== //

export default function MarkersPopups({ data }: Props) {
  const [popupInfo, setPopupInfo] = useState<CountryProps | null>(null);

  return (
    <RMap initialZoom={3.5} initialCenter={[78.96, 20.59]} mapStyle={osm_bright as StyleSpecification}>
      <RNavigationControl position="top-left" />
      {data.map((city, index) => (
        <RMarker
          key={`marker-${index}`}
          latitude={city.latlng[0]}
          longitude={city.latlng[1]}
          onClick={(event) => {
            event.stopPropagation();
            setPopupInfo(city);
          }}
        >
          <Box sx={{ cursor: 'pointer', width: 20, height: 20, backgroundColor: 'secondary.main', borderRadius: '50%' }} />
        </RMarker>
      ))}

      {popupInfo && (
        <RPopup
          longitude={popupInfo.latlng[1]}
          latitude={popupInfo.latlng[0]}
          offset={markerPopupOffset}
          onMapClick={() => setPopupInfo(null)}
        >
          <SubCard title={popupInfo.name}>
            <Stack>
              <Stack direction="row" sx={{ gap: 1, alignItems: 'center' }}>
                <Typography variant="subtitle1">Capital:</Typography>
                <Typography variant="body1">{popupInfo.capital}</Typography>
              </Stack>
              <Stack direction="row" sx={{ gap: 1, alignItems: 'center' }}>
                <Typography variant="subtitle1">Timezones:</Typography>
                <Typography variant="body1">{popupInfo.timezones}</Typography>
              </Stack>
              <Stack direction="row" sx={{ gap: 1, alignItems: 'center' }}>
                <Typography variant="subtitle1">Lat:</Typography>
                <Typography variant="body1">{popupInfo.latlng[0]}</Typography>
              </Stack>
              <Stack direction="row" sx={{ gap: 1, alignItems: 'center' }}>
                <Typography variant="subtitle1">Lng:</Typography>
                <Typography variant="body1">{popupInfo.latlng[1]}</Typography>
              </Stack>
            </Stack>
          </SubCard>
        </RPopup>
      )}
    </RMap>
  );
}
