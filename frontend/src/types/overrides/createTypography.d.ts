import '@mui/material/styles';

declare module '@mui/material/styles' {
  export type Variant = 'commonAvatar' | 'smallAvatar' | 'mediumAvatar' | 'largeAvatar';

  export interface TypographyVariantsOptions extends Partial<Record<Variant, TypographyStyleOptions>> {
    commonAvatar?: TypographyStyleOptions;
    smallAvatar?: TypographyStyleOptions;
    mediumAvatar?: TypographyStyleOptions;
    largeAvatar?: TypographyStyleOptions;
  }

  export interface TypographyVariants extends TypographyOptions {
    commonAvatar: TypographyStyle;
    smallAvatar: TypographyStyle;
    mediumAvatar: TypographyStyle;
    largeAvatar: TypographyStyle;
  }
}
