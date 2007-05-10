function is_not_empty (element)
{
	var permalink = map(itemgetter("id"), getElementsByTagAndClassName("span", "permalink", element));

	if (permalink.length >= 1)
	{
		return permalink[0];
	} else {
		return false;
	}
};

function toggle_permalink (d)
{
	var permalink = $(d.id);
	var permalink_span = is_not_empty(permalink);
	
	if (permalink_span)
	{
		removeElement($(permalink_span));
	} else {
		var span = SPAN({"id": "permalink-"+getNodeAttribute(permalink, "id")}, "¶"); //"&#182;"
		setElementClass(span, "permalink");
		insertSiblingNodesAfter(permalink.childNodes[0], span);
	}
};

function add_permalink (d)
{
	var permalink = $(d.id);
	var permalink_span = is_not_empty(permalink);

	if (!permalink_span)
	{
		var link = getNodeAttribute(permalink, "id");
		var span = SPAN({"id": "permalink-"+link}, A({"href": "#"+link}, "¶"));
		setElementClass(span, "permalink");
		insertSiblingNodesAfter(permalink.childNodes[0], span);
	}
};

l = true;
