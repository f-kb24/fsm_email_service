import baseStyled, { ThemedStyledInterface } from 'styled-components'

// styled-components/polished had way too much in library to justify the use for just darken and lighten

export const colors = {
    dark: '#0f141c',
}

export const theme = {
    colors: { ...colors },
}

export type Theme = typeof theme
export const styled = baseStyled as ThemedStyledInterface<Theme>
