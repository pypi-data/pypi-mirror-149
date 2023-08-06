/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import moment from 'moment';

export default {
  /** Wrap a value inside a list if the given value is not a list already. */
  asList(value) {
    if (!Array.isArray(value)) {
      return [value];
    }
    return value;
  },

  /** Capitalize a string. */
  capitalize(string) {
    if (string.length === 0) {
      return string;
    }
    return string.charAt(0).toUpperCase() + string.slice(1);
  },

  /** Scroll an element into the view using a specific alignment relative to it. */
  scrollIntoView(element, alignment = 'center') {
    if (alignment === 'top') {
      element.scrollIntoView(true);

      // Take the potentially fixed navigation header into account on larger screen sizes, based on the regular
      // Bootstrap breakpoints.
      const viewportWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
      if (viewportWidth >= 768) {
        window.scrollBy(0, element.getBoundingClientRect().top - 66);
      }
    } else if (alignment === 'bottom') {
      element.scrollIntoView(false);
    } else {
      element.scrollIntoView(false);
      const viewportHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
      const viewPortPercentage = element.getBoundingClientRect().top / viewportHeight;
      window.scrollBy(0, (viewPortPercentage - 0.5) * viewportHeight);
    }
  },

  /** Wrapper of the 'window.confirm' function for inline usage. */
  confirm(text, callback, ...args) {
    if (window.confirm(text)) {
      callback(...args);
    }
  },

  /**
   * Get a human-readable file size from a given amount of bytes.
   * Based on Jinja's 'filesizeformat' filter.
   */
  filesize(bytes) {
    const numBytes = Number.parseFloat(bytes, 10);
    const base = 1000;
    const prefixes = ['kB', 'MB', 'GB', 'TB', 'PB'];

    if (numBytes === 1) {
      return '1 Byte';
    } else if (numBytes < base) {
      return `${Math.floor(numBytes)} Bytes`;
    }

    let unit = 1;
    for (let i = 0; i < prefixes.length; i++) {
      unit = base ** (i + 2);
      if (numBytes < unit) {
        return `${Number(base * numBytes / unit).toFixed(1)} ${prefixes[i]}`;
      }
    }
    return `${Number(base * numBytes / unit).toFixed(1)} ${prefixes[prefixes.length - 1]}`;
  },

  /** Get a nested property of an object given a string specifying the property separated by dots. */
  getProp(object, property) {
    const props = property.split('.');
    let result = object;

    for (const prop of props) {
      result = result[prop];
    }
    return result;
  },

  /** Get one or multiple values of a search parameter of the current URL. */
  getSearchParam(param, getAll = false) {
    const url = new URL(window.location);
    const params = new URLSearchParams(url.search);

    if (getAll) {
      return params.getAll(param);
    }
    return params.get(param);
  },

  /** Check if the current URL contains a certain search parameter. */
  hasSearchParam(param) {
    const url = new URL(window.location);
    const params = new URLSearchParams(url.search);
    return params.has(param);
  },

  /** Insert a string at a given position inside another string. */
  insertString(string, index, toInsert) {
    if (index > 0) {
      return `${string.slice(0, index)}${toInsert}${string.slice(index)}`;
    }
    return toInsert + string;
  },

  /** Check if the type of an extra metadata entry is nested. */
  isNestedType(type) {
    return ['dict', 'list'].includes(type);
  },

  /** Paginate a list given a page and the amount of items per page. */
  paginateList(list, page, perPage) {
    const start = (page - 1) * perPage;
    const end = start + perPage;
    return list.slice(start, end);
  },

  /** Return a pretty type name based on a Python-like type string. */
  prettyTypeName(type) {
    switch (type) {
    case 'str': return 'string';
    case 'int': return 'integer';
    case 'bool': return 'boolean';
    case 'dict': return 'dictionary';
    default: return type;
    }
  },

  /** Generate a (not cryprographically secure) random alphanumeric string with a given length. */
  randomAlnum(length = 16) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars[Math.floor(Math.random() * chars.length)];
    }
    return result;
  },

  /** Remove all occurences of a given item from a list. */
  removeFromList(list, item) {
    let index = list.indexOf(item);
    while (index >= 0) {
      list.splice(index, 1);
      index = list.indexOf(item);
    }
  },

  /** Remove a single or all search parameter values of the current URL and return the new URL. */
  removeSearchParam(param, value = null) {
    const url = new URL(window.location);
    const params = new URLSearchParams(url.search);

    if (value === null) {
      params.delete(param);
    } else {
      const values = params.getAll(param);

      kadi.utils.removeFromList(values, String(value));
      params.delete(param);

      for (const value of values) {
        if (!params.has(param)) {
          params.set(param, value);
        } else {
          params.append(param, value);
        }
      }
    }

    url.search = params;
    return url;
  },

  /** Replace the current URL while retaining the old navigation history. */
  replaceState(url) {
    window.history.replaceState(null, '', url);
  },

  /** Replace or append values to a search parameter of the current URL and return the new URL. */
  setSearchParam(param, value, replace = true) {
    const url = new URL(window.location);
    const params = new URLSearchParams(url.search);

    if (replace || !params.has(param)) {
      params.set(param, value);
    } else {
      params.append(param, value);
    }

    url.search = params;
    return url;
  },

  /** Sleep for the given amount of milliseconds. */
  sleep(ms) {
    return new Promise((resolve) => window.setTimeout(resolve, ms));
  },

  /** Build a UTC timestamp from a given valid date string. */
  timestamp(datestring) {
    return moment.utc(datestring).format('YYYYMMDDHHmmss');
  },

  /** Truncate a string based on a given length. */
  truncate(string, length) {
    if (string.length > length) {
      return `${string.substring(0, length)}...`;
    }
    return string;
  },
};
