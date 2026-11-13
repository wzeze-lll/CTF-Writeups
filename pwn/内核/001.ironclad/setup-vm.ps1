<#
.SYNOPSIS
    Prepares a local Windows 11 26H2 VM that matches the remote Ironclad environment.

.DESCRIPTION
    Run elevated inside your VM, in this order:

      .\setup-vm.ps1 -Stage Check     what is installed and running now
      .\setup-vm.ps1 -Stage Boot      VBS/HVCI off, test signing on, no updates   (reboot)
      .\setup-vm.ps1 -Stage Check     confirm VBS is off and test signing is on
      .\setup-vm.ps1 -Stage Install   driver, placeholder flag, player account
      .\setup-vm.ps1 -Stage Verify    readiness report

    The remote VM runs with Secure Boot off, test signing on and VBS/HVCI not running.
    Turn Secure Boot off in your hypervisor's firmware settings: Windows ignores test
    signing while Secure Boot is on.

.PARAMETER Stage
    Check, Boot, Install or Verify.

.PARAMETER Payload
    Folder holding ironclad.sys (and optionally ironclad.cer).
    Defaults to the script's own folder.

.PARAMETER FlagText
    Contents of C:\flag.txt. Defaults to a placeholder.

.PARAMETER PlayerPassword
    Password for the unprivileged 'ctf' account.
#>
[CmdletBinding()]
param(
    [ValidateSet('Check', 'Boot', 'Install', 'Verify')]
    [string] $Stage = 'Check',
    [string] $Payload = $PSScriptRoot,
    [string] $FlagText = 'flag{local_placeholder}',
    [string] $PlayerPassword = 'Ironclad!2026',
    [string] $PlayerName = 'ctf',
    [string] $ServiceName = 'ironclad'
)

$ErrorActionPreference = 'Stop'

function Say    { param($m) Write-Host "    $m" }
function Step   { param($m) Write-Host "`n== $m" -ForegroundColor Cyan }
function Good   { param($m) Write-Host "  + $m" -ForegroundColor Green }
function Bad    { param($m) Write-Host "  - $m" -ForegroundColor Red }
function Warn   { param($m) Write-Host "  ! $m" -ForegroundColor Yellow }

function Assert-Elevated {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    $pr = New-Object Security.Principal.WindowsPrincipal($id)
    if (-not $pr.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw 'Run this script from an elevated PowerShell prompt.'
    }
}

function Get-GuardState {
    try {
        Get-CimInstance -Namespace root\Microsoft\Windows\DeviceGuard `
                        -ClassName Win32_DeviceGuard -ErrorAction Stop
    } catch {
        $null
    }
}

# ---------------------------------------------------------------- Check

function Invoke-Check {
    Step 'Build'
    $cv = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
    Say ("{0}  build {1}.{2}  {3}" -f $cv.DisplayVersion, $cv.CurrentBuild, $cv.UBR, $cv.EditionID)
    foreach ($f in @('ntoskrnl.exe')) {
        $p = Join-Path $env:SystemRoot "System32\$f"
        if (Test-Path $p) {
            $i = (Get-Item $p).VersionInfo
            Say ("{0,-22} {1}" -f (Split-Path $f -Leaf), $i.FileVersion)
            Say ("{0,-22} sha256 {1}" -f '', (Get-FileHash $p -Algorithm SHA256).Hash)
        }
    }

    Step 'Virtualization-based security (remote VM: not running)'
    $g = Get-GuardState
    if (-not $g) {
        Warn 'Device Guard information is unavailable'
    } else {
        $vbs = switch ($g.VirtualizationBasedSecurityStatus) {
            0 { 'off' } 1 { 'enabled but not running' } 2 { 'running' } default { 'unknown' }
        }
        if ($g.VirtualizationBasedSecurityStatus -eq 2) { Bad "VBS $vbs (remote VM: off)" } else { Good "VBS $vbs" }
        if ($g.SecurityServicesRunning -contains 2) { Bad 'HVCI running (remote VM: off)' } else { Good 'HVCI not running' }
    }

    Step 'Signing and updates'
    $bcd = (bcdedit /enum '{current}') -join "`n"
    if ($bcd -match 'testsigning\s+Yes') { Good 'test signing on' } else { Bad 'test signing off' }
    if ($bcd -match 'hypervisorlaunchtype\s+(\w+)') { Say "hypervisor launch: $($Matches[1]) (remote VM: no hypervisor)" }
    $au = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU'
    if ((Test-Path $au) -and (Get-ItemProperty $au).NoAutoUpdate -eq 1) {
        Good 'automatic updates disabled'
    } else {
        Warn 'automatic updates are not disabled: the build could move'
    }

    Step 'Challenge state'
    $svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($svc) { Say "service $ServiceName : $($svc.Status)" } else { Say "service $ServiceName not installed" }
    if (Test-Path '\\.\Ironclad') { Good 'device \\.\Ironclad present' } else { Say 'device not present' }
    if (Test-Path 'C:\flag.txt') { Good 'C:\flag.txt present' } else { Say 'C:\flag.txt missing' }
    if (Get-LocalUser -Name $PlayerName -ErrorAction SilentlyContinue) {
        Good "account $PlayerName exists"
    } else {
        Say "account $PlayerName missing"
    }
}

# ----------------------------------------------------------------- Boot

function Invoke-Boot {
    Assert-Elevated

    Step 'Turning VBS and memory integrity off (as in the remote VM)'
    $dg = 'HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard'
    if (-not (Test-Path $dg)) { New-Item -Path $dg | Out-Null }
    New-ItemProperty -Path $dg -Name EnableVirtualizationBasedSecurity -Value 0 -PropertyType DWord -Force | Out-Null
    $ci = "$dg\Scenarios\HypervisorEnforcedCodeIntegrity"
    if (-not (Test-Path $ci)) { New-Item -Path $ci -Force | Out-Null }
    New-ItemProperty -Path $ci -Name Enabled -Value 0 -PropertyType DWord -Force | Out-Null
    Good 'VBS and HVCI off'

    Step 'Boot configuration'
    bcdedit /set '{current}' testsigning on               | Out-Null
    bcdedit /set '{current}' hypervisorlaunchtype off     | Out-Null
    bcdedit /set '{current}' nointegritychecks off        | Out-Null
    Good 'test signing on, hypervisor off'

    Step 'Freezing the build'
    $au = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU'
    New-Item -Path $au -Force | Out-Null
    New-ItemProperty -Path $au -Name NoAutoUpdate -Value 1 -PropertyType DWord -Force | Out-Null
    foreach ($s in 'wuauserv', 'UsoSvc', 'WaaSMedicSvc') {
        try {
            Stop-Service $s -Force -ErrorAction SilentlyContinue
            Set-Service  $s -StartupType Disabled -ErrorAction SilentlyContinue
        } catch { }
    }
    Good 'Windows Update disabled'

    Step 'Crash behaviour'
    $cc = 'HKLM:\SYSTEM\CurrentControlSet\Control\CrashControl'
    New-ItemProperty -Path $cc -Name AutoReboot  -Value 1 -PropertyType DWord -Force | Out-Null
    New-ItemProperty -Path $cc -Name CrashDumpEnabled -Value 1 -PropertyType DWord -Force | Out-Null
    Good 'automatic restart on bugcheck, kernel dump kept'

    Write-Host "`nReboot now, then run: .\setup-vm.ps1 -Stage Check" -ForegroundColor Yellow
}

# -------------------------------------------------------------- Install

function Invoke-Install {
    Assert-Elevated

    $sys = Join-Path $Payload 'ironclad.sys'
    $cer = Join-Path $Payload 'ironclad.cer'
    if (-not (Test-Path $sys)) { throw "ironclad.sys not found in $Payload" }

    Step 'Prerequisites'
    $bcd = (bcdedit /enum '{current}') -join "`n"
    if ($bcd -notmatch 'testsigning\s+Yes') {
        throw 'Test signing is off. Run -Stage Boot, turn Secure Boot off and reboot first.'
    }
    Good 'test signing on'

    Step 'Test certificate'
    if (Test-Path $cer) {
        foreach ($store in 'Root', 'TrustedPublisher') {
            Import-Certificate -FilePath $cer -CertStoreLocation "Cert:\LocalMachine\$store" | Out-Null
        }
        Good 'certificate trusted as root and publisher'
    } else {
        Warn 'ironclad.cer not supplied; the driver must already be trusted'
    }

    Step 'Driver'
    $target = Join-Path $env:SystemRoot "System32\drivers\ironclad.sys"
    Copy-Item $sys $target -Force
    Say "sha256 $((Get-FileHash $target -Algorithm SHA256).Hash)"
    if (Get-Service -Name $ServiceName -ErrorAction SilentlyContinue) {
        sc.exe stop   $ServiceName | Out-Null
        sc.exe delete $ServiceName | Out-Null
        Start-Sleep -Seconds 1
    }
    $createOutput = (sc.exe create $ServiceName type= kernel start= auto binPath= $target 2>&1) -join ' '
    if ($LASTEXITCODE -ne 0) {
        Bad "could not register the service: $createOutput"
        Say 'run this script from an elevated prompt'
        return
    }
    $startOutput = (sc.exe start $ServiceName 2>&1) -join ' '
    $startCode = $LASTEXITCODE
    Start-Sleep -Seconds 1
    $svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue

    if ($svc -and $svc.Status -eq 'Running') {
        Good 'driver loaded'
    } else {
        Bad "driver did not start (service status $(if ($svc) { $svc.Status } else { 'absent' }), sc exit $startCode)"
        if ($startOutput -match 'FAILED\s+(\d+)') {
            $win32 = [int]$Matches[1]
            Say ("Windows error {0}: {1}" -f $win32, [ComponentModel.Win32Exception]::new($win32).Message)
            switch ($win32) {
                577  { Say 'cause: the signature was rejected. Confirm test signing is on and Secure Boot is off, then reboot.' }
                1275 { Say 'cause: blocked by policy. Memory integrity can refuse a driver; run -Stage Boot and reboot.' }
                31   { Say 'cause: DriverEntry returned a failure.' }
                1058 { Say 'cause: the service is disabled.' }
                2    { Say "cause: $target is missing." }
                default { Say 'see the events below.' }
            }
        }

        # DriverEntry failures surface as Service Control Manager events; the
        # kernel logs its own reason for refusing an image separately.
        Say ''
        Say 'recent related events:'
        $since = (Get-Date).AddMinutes(-5)
        $events = @()
        foreach ($log in 'System') {
            $events += Get-WinEvent -FilterHashtable @{
                LogName = $log; StartTime = $since
            } -ErrorAction SilentlyContinue |
                Where-Object { $_.Message -match 'ironclad|Code Integrity|integrity' } |
                Select-Object -First 6
        }
        if ($events) {
            foreach ($e in $events) {
                Say ("  [{0}] {1}: {2}" -f $e.TimeCreated.ToString('HH:mm:ss'),
                                           $e.ProviderName,
                                           ($e.Message -split "`n")[0].Trim())
            }
        } else {
            Say '  (none found; check Event Viewer under Windows Logs > System)'
        }
        Say ''
        Say 'Re-run -Stage Check.'
    }

    Step 'Flag'
    Set-Content -Path 'C:\flag.txt' -Value $FlagText -Encoding ASCII -NoNewline
    $acl = New-Object System.Security.AccessControl.FileSecurity
    $acl.SetAccessRuleProtection($true, $false)
    $sys = New-Object System.Security.Principal.NTAccount('NT AUTHORITY\SYSTEM')
    $acl.SetOwner($sys)
    $acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
        $sys, 'FullControl', 'Allow')))
    Set-Acl -Path 'C:\flag.txt' -AclObject $acl
    Good 'C:\flag.txt readable only by SYSTEM'

    Step 'Player account'
    $pw = ConvertTo-SecureString $PlayerPassword -AsPlainText -Force
    if (Get-LocalUser -Name $PlayerName -ErrorAction SilentlyContinue) {
        Set-LocalUser -Name $PlayerName -Password $pw
    } else {
        New-LocalUser -Name $PlayerName -Password $pw -AccountNeverExpires -PasswordNeverExpires | Out-Null
    }
    Add-LocalGroupMember -Group 'Users' -Member $PlayerName -ErrorAction SilentlyContinue
    foreach ($g in 'Administrators', 'Power Users') {
        Remove-LocalGroupMember -Group $g -Member $PlayerName -ErrorAction SilentlyContinue
    }
    Good "$PlayerName is an unprivileged standard user"

    Step 'Defender (remote VM: on, default settings)'
    try {
        if ((Get-MpComputerStatus -ErrorAction Stop).RealTimeProtectionEnabled) {
            Good 'real-time protection on'
        } else {
            Warn 'real-time protection is off; the remote VM keeps Defender on'
        }
    } catch {
        Warn 'could not read the Defender status'
    }

    Write-Host "`nNow run: .\setup-vm.ps1 -Stage Verify" -ForegroundColor Yellow
}

# --------------------------------------------------------------- Verify

function Invoke-Verify {
    $fail = 0

    Step 'Environment'
    $g = Get-GuardState
    if ($g -and $g.VirtualizationBasedSecurityStatus -eq 2) { Bad 'VBS running (remote VM: off)'; $fail++ } else { Good 'VBS not running' }
    $bcd = (bcdedit /enum '{current}') -join "`n"
    if ($bcd -match 'testsigning\s+Yes') { Good 'test signing on' } else { Bad 'test signing off'; $fail++ }

    Step 'Driver'
    $svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($svc -and $svc.Status -eq 'Running') { Good 'service running' } else { Bad 'service not running'; $fail++ }

    Step 'Flag'
    if (Test-Path 'C:\flag.txt') {
        $acl = Get-Acl 'C:\flag.txt'
        $who = $acl.Access | ForEach-Object { $_.IdentityReference.Value }
        Say ("access: {0}" -f ($who -join ', '))
        if ($who -contains 'NT AUTHORITY\SYSTEM' -and $who.Count -eq 1) {
            Good 'only SYSTEM can read the flag'
        } else {
            Bad 'the flag is readable by more than SYSTEM'; $fail++
        }
    } else {
        Bad 'C:\flag.txt missing'; $fail++
    }

    Step 'Player account'
    if (Get-LocalUser -Name $PlayerName -ErrorAction SilentlyContinue) {
        $admins = (Get-LocalGroupMember -Group 'Administrators' -ErrorAction SilentlyContinue |
                   ForEach-Object { $_.Name })
        if ($admins -match "\\$PlayerName$") {
            Bad "$PlayerName is an administrator"; $fail++
        } else {
            Good "$PlayerName is unprivileged"
        }
    } else {
        Bad "account $PlayerName missing"; $fail++
    }

    Write-Host ''
    if ($fail -eq 0) {
        Write-Host 'Local VM matches the remote environment.' -ForegroundColor Green
    } else {
        Write-Host "$fail problem(s) to fix before this VM can host the challenge." -ForegroundColor Red
    }
    exit $fail
}

switch ($Stage) {
    'Check'   { Invoke-Check }
    'Boot'    { Invoke-Boot }
    'Install' { Invoke-Install }
    'Verify'  { Invoke-Verify }
}
