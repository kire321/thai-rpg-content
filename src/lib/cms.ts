export const CMS_BASE = (import.meta.env.VITE_CMS_BASE || '/cms').replace(/\/$/, '')

export function cmsAsset(path: string): string {
  if (/^(https?:)?\//.test(path) && !path.startsWith('/')) return path
  return `${CMS_BASE}/${path.replace(/^\//, '')}`
}

/**
 * Load a CMS table from the published same-origin mirror.  The root fallback
 * keeps `vite preview` useful when the app is previewed directly from this
 * repository instead of from the publisher's /cms-ui/ mirror.
 */
export async function fetchCmsJson<T>(filename: string): Promise<T> {
  const candidates = [...new Set([`${CMS_BASE}/${filename}`, `/${filename}`])]
  let lastError: Error | null = null

  for (const url of candidates) {
    try {
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`)
      }
      return (await response.json()) as T
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error))
    }
  }

  throw lastError || new Error(`Unable to load ${filename}`)
}
