// Arrow-key navigation of a worklist (the review queue, the golden set): the
// reviewer keys straight through the rows without clicking one first. Pure
// functions; the lists bind the key handler on the window.

/** How many rows a key moves the selection by, or null when it is not a navigation key. */
export function navDelta(key, length) {
  switch (key) {
    case 'ArrowDown':
      return 1;
    case 'ArrowUp':
      return -1;
    case 'PageDown':
      return 10;
    case 'PageUp':
      return -10;
    case 'Home':
      return -length;
    case 'End':
      return length;
    default:
      return null;
  }
}

/**
 * The row to select after moving `delta` from `current` (-1 = nothing
 * selected, or the selection left the list): with nothing selected, enter the
 * list from the end the reviewer is arrowing towards; otherwise clamp.
 */
export function stepIndex(current, delta, length) {
  if (!length) return -1;
  if (current === -1) return delta > 0 ? 0 : length - 1;
  return Math.min(length - 1, Math.max(0, current + delta));
}

/** A key event the list may act on: no modifier held. */
export function plainKey(event) {
  return !(event.altKey || event.ctrlKey || event.metaKey || event.shiftKey);
}
