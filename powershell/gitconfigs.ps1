# Designed to be added to $PROFILE
# Information on using it as a script is at the bottom of the file

function Show-GitConfigs {
    # Function to parse git config output into a hashtable
    function Get-GitConfig {
        param ([string]$configLevel)
        $config = @{}
        git config $configLevel -l | ForEach-Object {
            $key, $value = $_ -split '=', 2
            $config[$key] = $value
        }
        return $config
    }

    # Collect configurations
    $systemConfig = Get-GitConfig --system
    $globalConfig = Get-GitConfig --global
    $localConfig = Get-GitConfig --local

    # Display configurations with colors
    Write-Host "System Configuration:" -ForegroundColor Yellow
    $systemConfig.GetEnumerator() | Sort-Object Key | ForEach-Object { "    $($_.Key) = $($_.Value)" }
    Write-Host ""

    Write-Host "Global Configuration:" -ForegroundColor Green
    $globalConfig.GetEnumerator() | Sort-Object Key | ForEach-Object { "    $($_.Key) = $($_.Value)" }
    Write-Host ""

    Write-Host "Local Configuration:" -ForegroundColor Cyan
    $localConfig.GetEnumerator() | Sort-Object Key | ForEach-Object { "    $($_.Key) = $($_.Value)" }
    Write-Host ""

    # Determine effective configuration and source
    $effectiveConfig = @{}
    $systemConfig.GetEnumerator() | ForEach-Object { $effectiveConfig[$_.Key] = @{ Value=$_.Value; Source='System'; Overridden=$false } }
    $globalConfig.GetEnumerator() | ForEach-Object { 
        if ($effectiveConfig.ContainsKey($_.Key)) { $effectiveConfig[$_.Key].Overridden = $true }
        $effectiveConfig[$_.Key] = @{ Value=$_.Value; Source='Global'; Overridden=$effectiveConfig[$_.Key].Overridden }
    }
    $localConfig.GetEnumerator() | ForEach-Object { 
        if ($effectiveConfig.ContainsKey($_.Key)) { $effectiveConfig[$_.Key].Overridden = $true }
        $effectiveConfig[$_.Key] = @{ Value=$_.Value; Source='Local'; Overridden=$effectiveConfig[$_.Key].Overridden }
    }

    # Display effective configuration with source-based color for overridden properties
    Write-Host "Effective Configuration:" -ForegroundColor Magenta
    $effectiveConfig.GetEnumerator() | Sort-Object Key | ForEach-Object {
        $color = if ($_.Value.Overridden) {
            switch ($_.Value.Source) {
                'Local' { 'Cyan' }
                'Global' { 'Green' }
                'System' { 'Yellow' }
            }
        } else { 'White' }
        
        Write-Host "    $($_.Key) = $($_.Value.Value)" -ForegroundColor $color
    }
}

Set-Alias -Name gitconfigs -Value Show-GitConfigs

# Comment out the line above and uncomment the line below to run this file as a script. You will likely need to set -ExecutionPolicy to Bypass to run this as a script.  pwsh -ExecutionPolicy Bypass -File .\gitconfigs.ps1

#Show-GitConfigs
