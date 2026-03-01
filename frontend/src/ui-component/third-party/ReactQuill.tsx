'use client';

// next
import dynamic from 'next/dynamic';

// material-ui
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';

const ReactQuill = dynamic(() => import('react-quill-new'), { ssr: false });

// third party
import 'react-quill-new/dist/quill.snow.css';

// project imports
import { ThemeDirection } from 'config';
import useConfig from 'hooks/useConfig';
import { withAlpha } from 'utils/colorUtils';

interface ReactQuillProps {
  value?: string;
  editorMinHeight?: number;
  onChange?: (value: string) => void;
}

// ==============================|| QUILL EDITOR ||============================== //

export default function ReactQuillDemo({ value, editorMinHeight = 125, onChange }: ReactQuillProps) {
  const {
    state: { fontFamily }
  } = useConfig();
  const theme = useTheme();

  return (
    <Box
      sx={{
        '& .quill': {
          bgcolor: 'grey.50',
          borderRadius: '12px',
          '& .ql-toolbar': {
            bgcolor: 'grey.100',
            borderColor: 'primary.light',
            borderTopLeftRadius: '12px',
            borderTopRightRadius: '12px',
            '& .ql-picker-options': {
              backgroundColor: 'background.paper',
              borderColor: `${theme.vars.palette.divider} !important`,
              borderRadius: '8px',
              color: 'text.primary',
              '& .ql-picker-item:hover': {
                color: theme.vars.palette.secondary.main
              }
            },
            '& .ql-formats': {
              'button:hover, button.ql-active': {
                '& .ql-stroke': { stroke: theme.vars.palette.secondary.main },
                '& .ql-fill': { fill: theme.vars.palette.secondary.main }
              },
              '& .ql-expanded .ql-picker-label': {
                borderColor: `${theme.vars.palette.text.secondary} !important`,
                color: 'text.secondary',
                '& .ql-stroke': { stroke: theme.vars.palette.text.secondary },
                '& .ql-fill': { fill: theme.vars.palette.text.secondary }
              },
              '& .ql-picker-label:hover, & .ql-picker-label.ql-active': {
                color: 'secondary.main',
                'svg .ql-stroke': {
                  stroke: theme.vars.palette.secondary.main
                }
              }
            }
          },
          '& .ql-container': {
            fontFamily,
            borderColor: 'primary.light',
            borderBottomLeftRadius: '12px',
            borderBottomRightRadius: '12px',
            '& .ql-editor': { minHeight: editorMinHeight }
          }
        },
        ...(theme.direction === ThemeDirection.RTL && { '& .ql-snow .ql-picker-label::before ': { ml: 2 } }),

        ...theme.applyStyles('dark', {
          '& .quill': {
            bgcolor: 'dark.main',
            '& .ql-toolbar': {
              bgcolor: 'dark.light',
              borderColor: withAlpha(theme.vars.palette.dark.light, 0.2)
            },
            '& .ql-container': { borderColor: `${withAlpha(theme.vars.palette.dark.light, 0.2)} !important` }
          }
        })
      }}
    >
      <ReactQuill {...(value && { value })} {...(onChange && { onChange })} />
    </Box>
  );
}
