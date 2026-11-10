# Gallatin's MPN UDS configuration

Gallatin operates UDS Core for this deployment. These actions use the pinned Core 1.14.0 source. Apply them in Gallatin's Core overrides and realm configuration; they are separate from Horizon application values.

Keycloak chart paths below are relative to the chart root. In a Core bundle, use `packages[core].overrides.keycloak.keycloak.values[].path`. Keep the desired settings in version control. **Realm initialization values do not update an existing realm:** apply a controlled Admin API/UI migration as well, preserving accounts, clients and access.

| Control | Configuration action |
|---|---|
| Inactivity | Set `realmInitEnv.ACCOUNT_INACTIVITY_DAYS="35"`. In an existing realm, enable `disable-inactive-users` with `disable-user.after=35d`; retain approved emergency/service-account exceptions. |
| Concurrent sessions | Set `realmInitEnv.SSO_SESSION_MAX_PER_USER` to Gallatin's approved positive maximum; `0` disables the limit. Update the existing `uds-user-session-count` authenticator configuration to match. |
| Session lifetime | Set `realmInitEnv.SSO_SESSION_MAX_LIFESPAN="28800"` for the eight-hour cap and retain `SSO_SESSION_IDLE_TIMEOUT="600"`. Apply equivalent existing-realm session settings. |
| Notice and consent | Set `realmInitEnv.TERMS_AND_CONDITIONS_ENABLED=true`; use the shipped notice/theme. Enable the Terms and Conditions required action and its default action in an existing realm. |
| Required smartcard path | For the approved certificate-only scope, retain `realmAuthFlows.X509_AUTH_ENABLED=true` and disable password/social alternatives with `USERNAME_PASSWORD_AUTH_ENABLED=false` and `SOCIAL_AUTH_ENABLED=false`. Apply the equivalent existing-realm flow and preserve the approved emergency-access path. |
| Local CRL cache | Enable `realmInitEnv.X509_CRL_CHECKING_ENABLED` and `X509_CRL_ABORT_IF_NON_UPDATED`; set `X509_CRL_RELATIVE_PATH` to the mounted approved CRL files. Refresh files before expiry and retain fail-closed revocation behavior. |
| Password denylist | Mount a maintained corpus under `/opt/keycloak/data/password-blacklists`, add `passwordBlacklist(filename)` to the existing `realmInitEnv.PASSWORD_POLICY`, and preserve its other constraints. The native provider reloads changed files; Gallatin supplies the update process. |
| Account notifications | Enable Keycloak `detailedObservability.alerts.enabled`. Set the Prometheus stack's Alertmanager receivers/routes and required notification egress for named security/operations recipients. UDS already supplies structured identity events and account alert rules. |
| Audit/runtime alerts | Configure specific audit-capacity and collection-failure rules in Prometheus/Alertmanager. Configure `falcosidekick.config.alertmanager.hostport` and endpoint for applicable Falco delivery, with explicit receivers and response actions. |
| Registry transport | Select the pinned Zarf init proxy mode (`uds zarf init --registry-mode=proxy`) for built-in cross-node mTLS, or explicitly configure a trusted TLS 1.2+ external registry. Proxy mode is alpha in Zarf 0.86; choose the supported path for MPN and plan migration for an initialized cluster. The default HTTP NodePort path does not meet the transport check. |
| Registry maintenance | Integrate the existing `uds zarf tools registry prune` into controlled post-upgrade maintenance. Preserve deployed images and approved rollback references; do not prune blindly during an active rollout. |
| Host/storage encryption | Select MPN's encrypted datastore, Secret-encryption provider and encrypted PVC/object-storage backend. UDS Core assumes an existing cluster/default StorageClass and does not choose the host's encryption implementation. Record these choices in Gallatin's deployment configuration. |

Minimum password-change age, character-difference enforcement and previous-login display have no matching shipped Core flag identified. Resolve them through supported provider extensions or accepted account-policy tailoring. Numeric limits, recipients, approved CAs/CRLs and account exceptions remain explicit Gallatin security decisions.

Sources: [Core Keycloak values](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/keycloak/chart/values.yaml), [Core override mapping](https://github.com/defenseunicorns/uds-core/blob/c15677633cffa17e99656a7d7ccd1f98d7cb6e4d/src/keycloak/common/zarf.yaml), and the per-rule links in the [evidence catalog](evidence/catalog.json).
