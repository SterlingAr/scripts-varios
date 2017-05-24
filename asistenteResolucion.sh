# El script sirve para añadir nuevas resoluciones de manera interactiva 
# En linux, puedo hacer eso usando los comandos 'cvt', 'xrandr', en este script quiero automatizar  este proceso
#
#
#
#

#guardo en una lista los displays conectados
connectedDisplays=($(xrandr | grep -w connected  | awk -F'[ +]' '{print $1}'))
#salvaguardo la resolución actual, guardo en 2 variables los valores actuales del eje X y Y respectivamente
Xaxis=$(xrandr --current | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f1) #

Yaxis=$(xrandr --current | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f2)

echo "Selecciona el display sobre el que quieres trabajar."

count=0
for i in ${connectedDisplays[@]}
do

	echo "$count.$i"
	count=$((++count))
done

echo -n "Tu selección: "

read displayInput

if [ $displayInput -ge 0 ] || [ $displayInput -le ${#connectedDisplays[@]} ]
then

	echo "Has seleccionado el display: ${connectedDisplays[$displayInput]}"
	
	echo "Introduce la resolución (ej 1440 900):"
        read width height

        echo "Has introducido la siguiente resolución: ${width}x${height}.Deseas continuar?(S/N)"


	read userContinue 
	
	if [ "${userContinue,}" == "s" ] || [ "${userContinue,}" == "y" ]
	then


        	fullModline=$(cvt $width $height | grep "Modeline" -A 5)
		echo $fullModline > $HOME/modeline.txt
        	modeline=$(grep -oP '(?<=Modeline ).*' ~/modeline.txt)
		lessModeline=$(sed '/Modeline/s/.*Modeline \([^ ][^ ]*\)[ ]*.*/\1/' ~/modeline.txt)
		xrandr --newmode $modeline
		xrandr --addmode ${connectedDisplays[$displayInput]} $lessModeline
		echo "La resolución se ha añadido, desea aplicarla? S/N"
		
		read changeRes
		
		if [ "${changeRes,}" == "s" ] || [ "${changeRes,}" == "y" ]
		then
			xrandr -s "${width}x${height}"
			echo "La resolución se ha aplicado.Desea revertir los cambios? S/N"
			
			read revertChanges
			if [ "${revertChanges,}" == "s" ] || [ "${revertChanges,}" == "y" ]
			then
				xrandr -s "${Xaxis}x${Yaxis}"
			else
				exit
			fi 
		else
			exit
		fi					

		
	else

	echo "Has salido del programa."
	exit
	fi
else

	echo "Input inválido."
	exit
fi


