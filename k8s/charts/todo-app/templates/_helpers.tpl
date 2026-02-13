{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s" $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "todo-app.backend.selectorLabels" -}}
app: todo-app
component: backend
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "todo-app.frontend.selectorLabels" -}}
app: todo-app
component: frontend
{{- end }}

{{/*
Backend labels
*/}}
{{- define "todo-app.backend.labels" -}}
{{ include "todo-app.labels" . }}
{{ include "todo-app.backend.selectorLabels" . }}
tier: api
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "todo-app.frontend.labels" -}}
{{ include "todo-app.labels" . }}
{{ include "todo-app.frontend.selectorLabels" . }}
tier: web
{{- end }}

{{/*
Notification Service selector labels
*/}}
{{- define "todo-app.notificationService.selectorLabels" -}}
app: todo-app
component: notification-service
{{- end }}

{{/*
Notification Service labels
*/}}
{{- define "todo-app.notificationService.labels" -}}
{{ include "todo-app.labels" . }}
{{ include "todo-app.notificationService.selectorLabels" . }}
tier: consumer
{{- end }}

{{/*
Recurring Task Service selector labels
*/}}
{{- define "todo-app.recurringTaskService.selectorLabels" -}}
app: todo-app
component: recurring-task-service
{{- end }}

{{/*
Recurring Task Service labels
*/}}
{{- define "todo-app.recurringTaskService.labels" -}}
{{ include "todo-app.labels" . }}
{{ include "todo-app.recurringTaskService.selectorLabels" . }}
tier: consumer
{{- end }}

{{/*
Audit Service selector labels
*/}}
{{- define "todo-app.auditService.selectorLabels" -}}
app: todo-app
component: audit-service
{{- end }}

{{/*
Audit Service labels
*/}}
{{- define "todo-app.auditService.labels" -}}
{{ include "todo-app.labels" . }}
{{ include "todo-app.auditService.selectorLabels" . }}
tier: consumer
{{- end }}

{{/*
WebSocket Service selector labels
*/}}
{{- define "todo-app.websocketService.selectorLabels" -}}
app: todo-app
component: websocket-service
{{- end }}

{{/*
WebSocket Service labels
*/}}
{{- define "todo-app.websocketService.labels" -}}
{{ include "todo-app.labels" . }}
{{ include "todo-app.websocketService.selectorLabels" . }}
tier: consumer
{{- end }}
