/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright held by original author
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation; either version 2 of the License, or (at your
    option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM; if not, write to the Free Software Foundation,
    Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

\*---------------------------------------------------------------------------*/

#include "degenerateMatcher.H"

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

Foam::hexMatcher Foam::degenerateMatcher::hex;
Foam::wedgeMatcher Foam::degenerateMatcher::wedge;
Foam::prismMatcher Foam::degenerateMatcher::prism;
Foam::tetWedgeMatcher Foam::degenerateMatcher::tetWedge;
Foam::pyrMatcher Foam::degenerateMatcher::pyr;
Foam::tetMatcher Foam::degenerateMatcher::tet;


Foam::cellShape Foam::degenerateMatcher::match
(
    const faceList& faces,
    const labelList& owner,
    const label cellI,
    const labelList& cellFaces
)
{
    // Recognize in order of assumed occurrence.

    if (hex.matchShape(false, faces, owner, cellI, cellFaces))
    {
        return cellShape(hex.model(), hex.vertLabels());
    }
    else if (tet.matchShape(false, faces, owner, cellI, cellFaces))
    {
        return cellShape(tet.model(), tet.vertLabels());
    }
    else if (prism.matchShape(false, faces, owner, cellI, cellFaces))
    {
        return cellShape(prism.model(), prism.vertLabels());
    }
    else if (pyr.matchShape(false, faces, owner, cellI, cellFaces))
    {
        return cellShape(pyr.model(), pyr.vertLabels());
    }
    else if (wedge.matchShape(false, faces, owner, cellI, cellFaces))
    {
        return cellShape(wedge.model(), wedge.vertLabels());
    }
    else if (tetWedge.matchShape(false, faces, owner, cellI, cellFaces))
    {
        return cellShape(tetWedge.model(), tetWedge.vertLabels());
    }
    else
    {
        return cellShape(*(cellModeller::lookup(0)), labelList(0));
    }
}


Foam::cellShape Foam::degenerateMatcher::match(const faceList& faces)
{
    // Do as if single cell mesh; all faces are referenced by a single cell

    return match
    (
        faces, 
        labelList(faces.size(), 0),     // Cell 0 is owner of all faces
        0,                              // cell 0
        labelList(cellMatcher::makeIdentity(faces.size()))  // cell 0 consists
                                                            // of all faces
    );
}


Foam::cellShape Foam::degenerateMatcher::match(const cellShape& shape)
{
    return match(shape.collapsedFaces());
}


Foam::cellShape Foam::degenerateMatcher::match
(
    const primitiveMesh& mesh,
    const label cellI
)
{
    return match
    (
        mesh.faces(), 
        mesh.faceOwner(),
        cellI,
        mesh.cells()[cellI]
    );
}


// ************************************************************************* //
