context="GitLab CI Bridge"
description="$MESSAGE"
ci_state="$STATE"
target_url="${CI_PIPELINE_URL}"

body='
{
"context": "'$context'",
"description": "'$description'",
"state": "'$ci_state'",
"target_url": "'$target_url'"
}
'

curl --request POST \
--data "$body" \
--header "Accept: application/json" \
--header "Content-Type: application/json" \
"${INSTANCE}/api/v1/repos/${MAIN_REPO}/statuses/${CI_COMMIT_SHA}?token=${GITEA_SECRET}"
