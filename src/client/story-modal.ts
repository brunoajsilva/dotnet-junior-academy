/** The modal that shows one user story. It closes with the close button, Esc or a click outside it. */
import { query } from "./dom";

let openModal: HTMLElement | null = null;
let rowThatOpenedModal: Element | null = null;

export function openStoryModal(storyId: string): void {
  const modal = document.getElementById(`story-${storyId}`);
  if (!modal) return;
  closeStoryModal();
  modal.hidden = false;
  openModal = modal;
  rowThatOpenedModal = document.activeElement;
  document.documentElement.classList.add("modal-open");
  const card = query(".smodal-card", modal);
  card.scrollTop = 0;
  query<HTMLButtonElement>(".smodal-head .ibtn", modal).focus();
}

export function closeStoryModal(): void {
  if (!openModal) return;
  openModal.hidden = true;
  openModal = null;
  document.documentElement.classList.remove("modal-open");
  if (rowThatOpenedModal instanceof HTMLElement && document.contains(rowThatOpenedModal)) rowThatOpenedModal.focus();
  rowThatOpenedModal = null;
}
