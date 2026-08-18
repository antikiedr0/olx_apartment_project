import { useState } from "react";

export default function Formularz(){
    const [powierzchnia, setPowierzchnia] = useState("")
    const [liczba_pokoi, setLiczbaPokoi] = useState("")
    const [miasto, setMiasto] = useState("")
    const [rynek, setRynek] = useState("")
    const [rodzaj_zabudowy, setRodzajZabudowy] = useState("")
    const [umeblowane, setUmeblowane] = useState(false)
    const [wynik, setWynik] = useState(null)
    return (
        <div>
        <p>powierzchnia w m2</p>
        <input 
            value={powierzchnia}
            onChange={(e)=> setPowierzchnia(e.target.value)}
         />
 
        <p>liczba_pokoi</p>
        <input
            value={liczba_pokoi}
            onChange={(e)=>setLiczbaPokoi(e.target.value)}
        />
        <br />        
        <select
            value={miasto}
            onChange={(e)=>setMiasto(e.target.value)}
        >
            <option value="warszawa">Warszawa</option>
            <option value="krakow">Kraków</option>
            <option value="wroclaw">Wrocław</option>
            <option value="bydgoszcz">Bydgoszcz</option>
        </select>

        <select
            value={rynek}
            onChange={(e)=>setRynek(e.target.value)}
        >
            <option value="pierwotny">Pierwotny</option>
            <option value="wtorny">Wtórny</option>
        </select>

        <select
            value={rodzaj_zabudowy}
            onChange={(e)=>setRodzajZabudowy(e.target.value)}
        >
            <option value="apartament">Apartament</option>
            <option value="kamienica">Kamienica</option>
            <option value="blok">Blok</option>
    
        </select>
        <p>umeblowane</p> 
        <input type="checkbox" 
            checked={umeblowane}
            onChange={(e) => setUmeblowane(e.target.checked)}
        />
        <br />
        <button onClick={() => sendData(powierzchnia, liczba_pokoi, miasto, rynek, rodzaj_zabudowy, umeblowane, setWynik)}>
            Oblicz cene
        </button>
        {wynik && <p>Przewidywana cena: {wynik} PLN/m²</p>}
        </div>

       
    )
}

async function sendData(powierzchnia, liczba_pokoi, miasto, rynek, rodzaj_zabudowy, umeblowane, setWynik){
    const response = await fetch("http://localhost:5000/predict",
        {
            method: "POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({
                powierzchnia: parseInt(powierzchnia),
                liczba_pokoi: parseInt(liczba_pokoi),
                miasto: miasto,
                rynek: rynek,
                rodzaj_zabudowy: rodzaj_zabudowy,
                umeblowane: umeblowane,

            }),
        }
    )
    const data = await response.json()
    console.log(data)
    setWynik(data.cena_m2)
}