import { api } from "../../scripts/api.js";

const nichImageSelectedHandler = (event) => {
    const { node_id, value } = event.detail
	const node = app.graph._nodes.find(node => node.id === parseInt(node_id, 10))
	const widget = node.widgets.find(widget => widget.name === "selected_image_name")
    widget.value = value
    widget.inputEl.disabled = true
}

api.addEventListener("nich-image-selected", nichImageSelectedHandler);
