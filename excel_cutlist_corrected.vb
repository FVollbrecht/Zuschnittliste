' VBA-Modul: Zuschnittoptimierung (KORRIGIERT nach Python-Gegenprüfung)
Option Explicit

' Datentyp für Stange
Type Bar
    cuts() As Double        ' Array der Schnitte
    cutCount As Integer     ' Anzahl Schnitte
    totalUsed As Double     ' Gesamtlänge genutzt
    waste As Double         ' Reststück
    barLength As Double     ' Stangenlänge
End Type

Sub Zuschnittoptimierung()
    Dim wsInput As Worksheet, wsOutput As Worksheet
    Dim barLength As Double, kerf As Double, multiplier As Integer
    Dim lastRow As Long, i As Long, j As Long
    Dim cutList() As Double, bars() As Bar
    Dim barCount As Integer
    Dim algo As String
    Dim materialCode As String, materialName As String
    Dim materialDict As Object
    Dim key As Variant

    ' Parameter
    barLength = 6000 ' Standardlänge in mm
    kerf = 3 ' Sägeblattstärke in mm
    multiplier = 1 ' Stücklistenmultiplikator
    algo = "BFD" ' Alternativ: "FFD"

    Set wsInput = ThisWorkbook.Sheets("Stueckliste")
    Set wsOutput = ThisWorkbook.Sheets("Zuschnittplan")
    
    ' Material-Gruppierung vorbereiten
    Set materialDict = CreateObject("Scripting.Dictionary")
    
    lastRow = wsInput.Cells(wsInput.Rows.Count, 1).End(xlUp).Row

    ' Stückliste einlesen und nach Material gruppieren
    For i = 2 To lastRow
        Dim cutLength As Double
        Dim quantity As Integer
        
        cutLength = wsInput.Cells(i, 1).Value ' Spalte A: Länge
        quantity = wsInput.Cells(i, 2).Value ' Spalte B: Anzahl
        materialCode = wsInput.Cells(i, 3).Value ' Spalte C: Material
        materialName = wsInput.Cells(i, 4).Value ' Spalte D: Materialname
        
        ' Material-Gruppierung
        If Not materialDict.Exists(materialCode) Then
            materialDict.Add materialCode, Array(materialName, New Collection)
        End If
        
        ' Schnitte hinzufügen (mit Multiplikator)
        Dim matInfo As Variant
        matInfo = materialDict(materialCode)
        Dim matCuts As Collection
        Set matCuts = matInfo(1)
        
        For j = 1 To quantity * multiplier
            matCuts.Add cutLength
        Next j
        
        materialDict(materialCode) = Array(matInfo(0), matCuts)
    Next i

    ' Ergebnis ausgeben
    wsOutput.Cells.Clear
    wsOutput.Cells(1, 1).Value = "Material"
    wsOutput.Cells(1, 2).Value = "Materialname"
    wsOutput.Cells(1, 3).Value = "Stab Nr."
    wsOutput.Cells(1, 4).Value = "Schnitte"
    wsOutput.Cells(1, 5).Value = "Gesamt genutzt"
    wsOutput.Cells(1, 6).Value = "Reststück"
    wsOutput.Cells(1, 7).Value = "Effizienz %"
    
    Dim outputRow As Long
    outputRow = 2
    
    ' Optimierung für jedes Material
    For Each key In materialDict.Keys
        matInfo = materialDict(key)
        materialName = matInfo(0)
        Set matCuts = matInfo(1)
        
        ' Collection zu Array konvertieren
        ReDim cutList(1 To matCuts.Count)
        For i = 1 To matCuts.Count
            cutList(i) = matCuts(i)
        Next i
        
        ' Sortieren (absteigend)
        Call QuickSort(cutList, LBound(cutList), UBound(cutList))
        
        ' Optimierung durchführen
        If algo = "FFD" Then
            barCount = OptimizeFFD(cutList, bars, barLength, kerf)
        ElseIf algo = "BFD" Then
            barCount = OptimizeBFD(cutList, bars, barLength, kerf)
        End If
        
        ' Ergebnisse schreiben
        For i = 1 To barCount
            wsOutput.Cells(outputRow, 1).Value = key
            wsOutput.Cells(outputRow, 2).Value = materialName
            wsOutput.Cells(outputRow, 3).Value = i
            wsOutput.Cells(outputRow, 4).Value = JoinBarCuts(bars(i))
            wsOutput.Cells(outputRow, 5).Value = Round(bars(i).totalUsed, 1) & " mm"
            wsOutput.Cells(outputRow, 6).Value = Round(bars(i).waste, 1) & " mm"
            wsOutput.Cells(outputRow, 7).Value = Round(bars(i).totalUsed / bars(i).barLength * 100, 1) & "%"
            outputRow = outputRow + 1
        Next i
        
        ' Zusammenfassung für Material
        Dim totalWaste As Double, avgEfficiency As Double
        totalWaste = 0
        avgEfficiency = 0
        For i = 1 To barCount
            totalWaste = totalWaste + bars(i).waste
            avgEfficiency = avgEfficiency + (bars(i).totalUsed / bars(i).barLength * 100)
        Next i
        avgEfficiency = avgEfficiency / barCount
        
        wsOutput.Cells(outputRow, 3).Value = "Summe:"
        wsOutput.Cells(outputRow, 3).Font.Bold = True
        wsOutput.Cells(outputRow, 5).Value = barCount & " Stangen"
        wsOutput.Cells(outputRow, 6).Value = Round(totalWaste, 1) & " mm"
        wsOutput.Cells(outputRow, 7).Value = Round(avgEfficiency, 1) & "%"
        outputRow = outputRow + 2
    Next key
    
    MsgBox "Optimierung abgeschlossen!" & vbCrLf & _
           "Algorithmus: " & algo & vbCrLf & _
           "Materialien: " & materialDict.Count, vbInformation
End Sub

' First Fit Decreasing - KORRIGIERT
Function OptimizeFFD(cutList() As Double, bars() As Bar, barLength As Double, kerf As Double) As Integer
    Dim i As Long, barCount As Integer, placed As Boolean
    
    barCount = 0
    
    For i = LBound(cutList) To UBound(cutList)
        placed = False
        Dim cutLen As Double
        cutLen = cutList(i)
        
        ' Versuche in vorhandene Stangen zu platzieren
        Dim j As Integer
        For j = 1 To barCount
            ' KORRIGIERT: Kerf nur wenn nicht erster Schnitt
            Dim additionalLength As Double
            additionalLength = cutLen
            If bars(j).cutCount > 0 Then
                additionalLength = additionalLength + kerf
            End If
            
            If bars(j).totalUsed + additionalLength <= barLength Then
                ' Schnitt hinzufügen
                bars(j).cutCount = bars(j).cutCount + 1
                ReDim Preserve bars(j).cuts(1 To bars(j).cutCount)
                bars(j).cuts(bars(j).cutCount) = cutLen
                bars(j).totalUsed = bars(j).totalUsed + additionalLength
                bars(j).waste = barLength - bars(j).totalUsed
                placed = True
                Exit For
            End If
        Next j
        
        ' Neue Stange wenn nicht platziert
        If Not placed Then
            barCount = barCount + 1
            ReDim Preserve bars(1 To barCount)
            
            bars(barCount).cutCount = 1
            ReDim bars(barCount).cuts(1 To 1)
            bars(barCount).cuts(1) = cutLen
            bars(barCount).totalUsed = cutLen
            bars(barCount).barLength = barLength
            bars(barCount).waste = barLength - cutLen
        End If
    Next i
    
    OptimizeFFD = barCount
End Function

' Best Fit Decreasing - KORRIGIERT
Function OptimizeBFD(cutList() As Double, bars() As Bar, barLength As Double, kerf As Double) As Integer
    Dim i As Long, barCount As Integer
    Dim cutLen As Double
    
    barCount = 0
    
    For i = LBound(cutList) To UBound(cutList)
        cutLen = cutList(i)
        
        ' Finde beste Stange (kleinster Rest)
        Dim bestIdx As Integer, minWaste As Double
        bestIdx = 0
        minWaste = barLength + 1
        
        Dim j As Integer
        For j = 1 To barCount
            ' KORRIGIERT: Kerf nur wenn nicht erster Schnitt
            Dim additionalLength As Double
            additionalLength = cutLen
            If bars(j).cutCount > 0 Then
                additionalLength = additionalLength + kerf
            End If
            
            Dim remainingSpace As Double
            remainingSpace = barLength - bars(j).totalUsed
            
            If remainingSpace >= additionalLength Then
                Dim wasteAfter As Double
                wasteAfter = remainingSpace - additionalLength
                
                If wasteAfter < minWaste Then
                    minWaste = wasteAfter
                    bestIdx = j
                End If
            End If
        Next j
        
        ' Platziere in beste Stange oder erstelle neue
        If bestIdx > 0 Then
            ' In vorhandene Stange
            additionalLength = cutLen
            If bars(bestIdx).cutCount > 0 Then
                additionalLength = additionalLength + kerf
            End If
            
            bars(bestIdx).cutCount = bars(bestIdx).cutCount + 1
            ReDim Preserve bars(bestIdx).cuts(1 To bars(bestIdx).cutCount)
            bars(bestIdx).cuts(bars(bestIdx).cutCount) = cutLen
            bars(bestIdx).totalUsed = bars(bestIdx).totalUsed + additionalLength
            bars(bestIdx).waste = barLength - bars(bestIdx).totalUsed
        Else
            ' Neue Stange
            barCount = barCount + 1
            ReDim Preserve bars(1 To barCount)
            
            bars(barCount).cutCount = 1
            ReDim bars(barCount).cuts(1 To 1)
            bars(barCount).cuts(1) = cutLen
            bars(barCount).totalUsed = cutLen
            bars(barCount).barLength = barLength
            bars(barCount).waste = barLength - cutLen
        End If
    Next i
    
    OptimizeBFD = barCount
End Function

' Hilfsfunktion: Schnitte als Text
Function JoinBarCuts(bar As Bar) As String
    Dim cuts As String, i As Integer
    cuts = ""
    For i = 1 To bar.cutCount
        If i > 1 Then cuts = cuts & " / "
        cuts = cuts & Format(bar.cuts(i), "0.0") & "mm"
    Next i
    JoinBarCuts = cuts
End Function

' QuickSort für Stückliste (absteigend)
Sub QuickSort(arr() As Double, first As Long, last As Long)
    Dim i As Long, j As Long, pivot As Double, temp As Double
    i = first: j = last: pivot = arr((first + last) \ 2)
    Do While i <= j
        Do While arr(i) > pivot: i = i + 1: Loop
        Do While arr(j) < pivot: j = j - 1: Loop
        If i <= j Then
            temp = arr(i): arr(i) = arr(j): arr(j) = temp
            i = i + 1: j = j - 1
        End If
    Loop
    If first < j Then QuickSort arr, first, j
    If i < last Then QuickSort arr, i, last
End Sub
