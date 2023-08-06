curl \
	-d "For ${CI_COMMIT_SHORT_SHA} in ${MAIN_REPO}" \
	-H "Title: ${MESSAGE}" \
	-H "Priority: high" \
	https://ntfy.sh/$NTFY_SECRET
